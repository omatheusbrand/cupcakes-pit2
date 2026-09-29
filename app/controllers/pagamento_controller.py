"""
Controlador de pagamento (Controller, na sigla MVC).
Implementa o CU-02 (pagar pedido): US-12, US-13.
Pagamento SIMULADO nesta versão — não há integração com operadora real.
"""
import random
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Pedido, Pagamento, Cupcake

pagamento_bp = Blueprint("pagamento", __name__)


def _pedido_do_usuario_ou_404(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.usuario_id != session.get("usuario_id"):
        return None
    return pedido


@pagamento_bp.route("/pagamento/<int:pedido_id>")
def pagina_pagamento(pedido_id):
    pedido = _pedido_do_usuario_ou_404(pedido_id)
    if pedido is None:
        return redirect(url_for("vitrine.index"))
    if pedido.status != "aguardando_pagamento":
        return redirect(url_for("pedido.confirmacao", pedido_id=pedido.id))
    return render_template("pagamento.html", pedido=pedido)


@pagamento_bp.route("/pagamento/<int:pedido_id>/processar", methods=["POST"])
def processar(pedido_id):
    pedido = _pedido_do_usuario_ou_404(pedido_id)
    if pedido is None:
        return redirect(url_for("vitrine.index"))
    if pedido.status != "aguardando_pagamento":
        return redirect(url_for("pedido.confirmacao", pedido_id=pedido.id))

    metodo = request.form.get("metodo")

    if metodo == "pix":
        # Pix simulado: ao confirmar, consideramos pago (curso alternativo Alfa do CU-02)
        pagamento = Pagamento(
            pedido_id=pedido.id, metodo="pix", status="aprovado",
            valor=pedido.total, codigo_pix=f"PIX-SIMULADO-{random.randint(100000, 999999)}",
        )
        db.session.add(pagamento)
        _aprovar_pedido(pedido)
        return redirect(url_for("pedido.confirmacao", pedido_id=pedido.id))

    # metodo == "cartao"
    numero = request.form.get("numero_cartao", "").replace(" ", "")
    validade = request.form.get("validade", "").strip()
    cvv = request.form.get("cvv", "").strip()

    dados_validos = numero.isdigit() and len(numero) == 16 and validade and cvv.isdigit() and len(cvv) == 3

    if not dados_validos:
        # Curso alternativo Beta do CU-02: dados inválidos ou recusa
        pagamento = Pagamento(
            pedido_id=pedido.id, metodo="cartao", status="recusado", valor=pedido.total,
        )
        db.session.add(pagamento)
        db.session.commit()
        flash("Pagamento recusado. Confira os dados do cartão e tente novamente.", "erro")
        return redirect(url_for("pagamento.pagina_pagamento", pedido_id=pedido.id))

    pagamento = Pagamento(
        pedido_id=pedido.id, metodo="cartao", status="aprovado",
        valor=pedido.total, cartao_final=numero[-4:],  # RNF05: só os 4 últimos dígitos
    )
    db.session.add(pagamento)
    _aprovar_pedido(pedido)
    return redirect(url_for("pedido.confirmacao", pedido_id=pedido.id))


def _aprovar_pedido(pedido):
    """RN07: o pedido só é confirmado depois que o pagamento é aprovado."""
    pedido.status = "recebido"  # RN08
    for item in pedido.itens:
        cupcake = Cupcake.query.get(item.cupcake_id)
        cupcake.estoque = max(0, cupcake.estoque - item.quantidade)
    db.session.commit()
