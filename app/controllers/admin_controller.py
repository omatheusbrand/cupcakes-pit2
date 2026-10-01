"""
Controlador administrativo (Controller, na sigla MVC).
Implementa o CU-04 (cadastrar cupcake) e o CU-03 (atualizar status do pedido):
US-16 (gerenciar cupcakes) e US-17 (ver pedidos e atualizar status).
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Cupcake, Categoria, Pedido

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# RN08: ordem das etapas de um pedido
SEQUENCIA_STATUS = [
    "aguardando_pagamento", "recebido", "em_preparo",
    "saiu_para_entrega", "pronto_para_retirada", "entregue",
]
STATUS_LEGIVEL = {
    "aguardando_pagamento": "Aguardando pagamento",
    "recebido": "Recebido",
    "em_preparo": "Em preparo",
    "saiu_para_entrega": "Saiu para entrega",
    "pronto_para_retirada": "Pronto para retirada",
    "entregue": "Entregue",
    "cancelado": "Cancelado",
}


def _requer_admin():
    # Curso alternativo Alfa do CU-03/CU-04: só administrador acessa
    return session.get("usuario_papel") == "admin"


@admin_bp.before_request
def protege_area_admin():
    if not _requer_admin():
        flash("Acesso restrito ao administrador.", "erro")
        return redirect(url_for("vitrine.index"))


@admin_bp.route("/cupcakes")
def listar_cupcakes():
    cupcakes = Cupcake.query.order_by(Cupcake.nome).all()
    return render_template("admin_cupcakes.html", cupcakes=cupcakes)


@admin_bp.route("/cupcakes/novo", methods=["GET", "POST"])
def novo_cupcake():
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        erro = _validar_formulario_cupcake(request.form)
        if erro:
            flash(erro, "erro")
            return render_template("admin_form_cupcake.html", categorias=categorias, cupcake=None, dados=request.form)

        cupcake = Cupcake(
            categoria_id=request.form.get("categoria_id", type=int),
            nome=request.form.get("nome", "").strip(),
            descricao=request.form.get("descricao", "").strip(),
            ingredientes=request.form.get("ingredientes", "").strip(),
            alergenicos=request.form.get("alergenicos", "").strip() or None,
            preco=float(request.form.get("preco")),
            estoque=int(request.form.get("estoque", 0)),
            foto_url=request.form.get("foto_url", "").strip() or None,
            ativo=True,
        )
        db.session.add(cupcake)
        db.session.commit()
        flash(f"{cupcake.nome} cadastrado.", "sucesso")
        return redirect(url_for("admin.listar_cupcakes"))

    return render_template("admin_form_cupcake.html", categorias=categorias, cupcake=None, dados=None)


@admin_bp.route("/cupcakes/<int:cupcake_id>/editar", methods=["GET", "POST"])
def editar_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        erro = _validar_formulario_cupcake(request.form)
        if erro:
            flash(erro, "erro")
            return render_template("admin_form_cupcake.html", categorias=categorias, cupcake=cupcake, dados=request.form)

        cupcake.categoria_id = request.form.get("categoria_id", type=int)
        cupcake.nome = request.form.get("nome", "").strip()
        cupcake.descricao = request.form.get("descricao", "").strip()
        cupcake.ingredientes = request.form.get("ingredientes", "").strip()
        cupcake.alergenicos = request.form.get("alergenicos", "").strip() or None
        cupcake.preco = float(request.form.get("preco"))
        cupcake.estoque = int(request.form.get("estoque", 0))
        cupcake.foto_url = request.form.get("foto_url", "").strip() or None
        db.session.commit()
        flash(f"{cupcake.nome} atualizado.", "sucesso")
        return redirect(url_for("admin.listar_cupcakes"))

    return render_template("admin_form_cupcake.html", categorias=categorias, cupcake=cupcake, dados=None)


def _validar_formulario_cupcake(form):
    """RN03: preço deve ser maior que zero. Também exige os campos obrigatórios."""
    obrigatorios = ["nome", "descricao", "ingredientes", "categoria_id", "preco"]
    for campo in obrigatorios:
        if not form.get(campo, "").strip():
            return "Preencha todos os campos obrigatórios."
    try:
        preco = float(form.get("preco"))
    except ValueError:
        return "Preço inválido."
    if preco <= 0:  # RN03
        return "O preço deve ser maior que zero."
    try:
        estoque = int(form.get("estoque", 0))
    except ValueError:
        return "Estoque inválido."
    if estoque < 0:
        return "O estoque não pode ser negativo."
    return None


@admin_bp.route("/cupcakes/<int:cupcake_id>/alternar-status", methods=["POST"])
def alternar_status_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.ativo = not cupcake.ativo  # desativa em vez de apagar, preservando o histórico
    db.session.commit()
    flash(f"{cupcake.nome} {'ativado' if cupcake.ativo else 'desativado'}.", "sucesso")
    return redirect(url_for("admin.listar_cupcakes"))


@admin_bp.route("/pedidos")
def listar_pedidos():
    filtro = request.args.get("status")
    consulta = Pedido.query
    if filtro:
        consulta = consulta.filter_by(status=filtro)
    pedidos = consulta.order_by(Pedido.criado_em.desc()).all()
    return render_template(
        "admin_pedidos.html", pedidos=pedidos, filtro=filtro,
        sequencia=SEQUENCIA_STATUS, legivel=STATUS_LEGIVEL,
    )


@admin_bp.route("/pedidos/<int:pedido_id>/status", methods=["POST"])
def atualizar_status_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    novo_status = request.form.get("status")

    # RN08/RN09: não altera pedido já entregue ou cancelado
    if pedido.status in ("entregue", "cancelado"):
        flash("Este pedido não pode mais ser alterado.", "erro")
        return redirect(url_for("admin.listar_pedidos"))

    if novo_status not in SEQUENCIA_STATUS and novo_status != "cancelado":
        flash("Status inválido.", "erro")
        return redirect(url_for("admin.listar_pedidos"))

    pedido.status = novo_status
    db.session.commit()
    flash(f"Pedido #{pedido.id} atualizado para \"{STATUS_LEGIVEL[novo_status]}\".", "sucesso")
    return redirect(url_for("admin.listar_pedidos"))
