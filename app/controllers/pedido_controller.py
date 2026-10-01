"""
Controlador do pedido (Controller, na sigla MVC).
Implementa o CU-01 (finalizar pedido): US-09, US-10, US-11.
Segue o curso básico de ação e os cursos alternativos descritos em
docs/05-casos-de-uso-expandidos.md.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Endereco, Pedido, ItemPedido, Configuracao
from app.controllers.carrinho_controller import obter_itens_do_carrinho, calcular_subtotal

pedido_bp = Blueprint("pedido", __name__)


def usuario_logado():
    return session.get("usuario_id")


def obter_taxa_entrega():
    config = Configuracao.query.get(1)
    return config.taxa_entrega if config else 0


@pedido_bp.route("/pedido/entrega", methods=["GET", "POST"])
def escolher_entrega():
    # Curso alternativo Alfa do CU-01: exige login (RN05)
    if not usuario_logado():
        flash("Entre na sua conta para continuar o pedido.", "erro")
        return redirect(url_for("auth.login", proximo=url_for("pedido.escolher_entrega")))

    itens = obter_itens_do_carrinho()
    # Curso alternativo Beta do CU-01: carrinho vazio (RN04)
    if not itens:
        flash("Seu carrinho está vazio.", "erro")
        return redirect(url_for("carrinho.ver_carrinho"))

    enderecos = Endereco.query.filter_by(usuario_id=usuario_logado()).all()

    if request.method == "POST":
        tipo = request.form.get("tipo_recebimento")

        if tipo == "entrega":
            endereco_id = request.form.get("endereco_id", type=int)
            if not endereco_id:
                flash("Informe o endereço de entrega.", "erro")
                return render_template("entrega.html", enderecos=enderecos, taxa=obter_taxa_entrega())
            session["pedido_tipo_recebimento"] = "entrega"
            session["pedido_endereco_id"] = endereco_id
        else:
            # Curso alternativo Gama do CU-01: retirada não exige endereço (RN06)
            session["pedido_tipo_recebimento"] = "retirada"
            session["pedido_endereco_id"] = None

        return redirect(url_for("pedido.resumo"))

    return render_template("entrega.html", enderecos=enderecos, taxa=obter_taxa_entrega())


@pedido_bp.route("/pedido/endereco/novo", methods=["POST"])
def novo_endereco():
    if not usuario_logado():
        return redirect(url_for("auth.login"))

    endereco = Endereco(
        usuario_id=usuario_logado(),
        rua=request.form.get("rua", "").strip(),
        numero=request.form.get("numero", "").strip(),
        complemento=request.form.get("complemento", "").strip() or None,
        bairro=request.form.get("bairro", "").strip(),
        cidade=request.form.get("cidade", "").strip(),
        uf=request.form.get("uf", "").strip().upper()[:2],
        cep=request.form.get("cep", "").strip(),
    )
    db.session.add(endereco)
    db.session.commit()

    session["pedido_tipo_recebimento"] = "entrega"
    session["pedido_endereco_id"] = endereco.id
    flash("Endereço cadastrado.", "sucesso")
    return redirect(url_for("pedido.resumo"))


@pedido_bp.route("/pedido/resumo")
def resumo():
    if not usuario_logado():
        return redirect(url_for("auth.login"))

    itens = obter_itens_do_carrinho()
    if not itens:
        flash("Seu carrinho está vazio.", "erro")
        return redirect(url_for("carrinho.ver_carrinho"))

    tipo = session.get("pedido_tipo_recebimento")
    if not tipo:
        return redirect(url_for("pedido.escolher_entrega"))

    subtotal = calcular_subtotal(itens)
    taxa = obter_taxa_entrega() if tipo == "entrega" else 0  # RN06
    total = subtotal + taxa

    endereco = None
    if tipo == "entrega":
        endereco = Endereco.query.get(session.get("pedido_endereco_id"))

    return render_template(
        "resumo.html", itens=itens, subtotal=subtotal, taxa=taxa, total=total,
        tipo=tipo, endereco=endereco,
    )


@pedido_bp.route("/pedido/finalizar", methods=["POST"])
def finalizar():
    if not usuario_logado():
        return redirect(url_for("auth.login"))

    itens = obter_itens_do_carrinho()
    if not itens:
        flash("Seu carrinho está vazio.", "erro")
        return redirect(url_for("carrinho.ver_carrinho"))

    tipo = session.get("pedido_tipo_recebimento")
    if not tipo:
        return redirect(url_for("pedido.escolher_entrega"))

    # Curso alternativo Delta do CU-01: confere disponibilidade de cada item (RN10)
    for item in itens:
        if not item["cupcake"].disponivel or item["cupcake"].estoque < item["quantidade"]:
            flash(f"{item['cupcake'].nome} ficou indisponível. Ajuste o carrinho para continuar.", "erro")
            return redirect(url_for("carrinho.ver_carrinho"))

    subtotal = calcular_subtotal(itens)
    taxa = obter_taxa_entrega() if tipo == "entrega" else 0
    total = subtotal + taxa

    pedido = Pedido(
        usuario_id=usuario_logado(),
        endereco_id=session.get("pedido_endereco_id") if tipo == "entrega" else None,
        tipo_recebimento=tipo,
        subtotal=subtotal,
        taxa_entrega=taxa,
        total=total,
        status="aguardando_pagamento",
    )
    db.session.add(pedido)
    db.session.flush()  # gera o pedido.id antes de gravar os itens

    for item in itens:
        db.session.add(ItemPedido(
            pedido_id=pedido.id,
            cupcake_id=item["cupcake"].id,
            quantidade=item["quantidade"],
            preco_unitario=item["cupcake"].preco,  # guarda o preço do momento da compra
        ))

    db.session.commit()

    # Limpa o carrinho e os dados temporários de entrega
    session.pop("carrinho", None)
    session.pop("pedido_tipo_recebimento", None)
    session.pop("pedido_endereco_id", None)

    return redirect(url_for("pagamento.pagina_pagamento", pedido_id=pedido.id))


@pedido_bp.route("/pedido/<int:pedido_id>/confirmacao")
def confirmacao(pedido_id):
    if not usuario_logado():
        return redirect(url_for("auth.login"))

    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.usuario_id != usuario_logado():
        return redirect(url_for("vitrine.index"))

    return render_template("confirmacao.html", pedido=pedido)


@pedido_bp.route("/meus-pedidos")
def meus_pedidos():
    if not usuario_logado():
        return redirect(url_for("auth.login"))

    pedidos = (
        Pedido.query.filter_by(usuario_id=usuario_logado())
        .filter(Pedido.status != "aguardando_pagamento")  # só mostra pedidos já pagos
        .order_by(Pedido.criado_em.desc())
        .all()
    )
    return render_template("meus_pedidos.html", pedidos=pedidos)


@pedido_bp.route("/pedido/<int:pedido_id>/acompanhar")
def acompanhar(pedido_id):
    if not usuario_logado():
        return redirect(url_for("auth.login"))

    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.usuario_id != usuario_logado():
        return redirect(url_for("pedido.meus_pedidos"))

    etapas = ["recebido", "em_preparo", "saiu_para_entrega" if pedido.tipo_recebimento == "entrega" else "pronto_para_retirada", "entregue"]
    return render_template("acompanhar.html", pedido=pedido, etapas=etapas)


@pedido_bp.route("/pedido/<int:pedido_id>/cancelar", methods=["POST"])
def cancelar(pedido_id):
    if not usuario_logado():
        return redirect(url_for("auth.login"))

    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.usuario_id != usuario_logado():
        return redirect(url_for("pedido.meus_pedidos"))

    if not pedido.pode_cancelar:  # RN09: só antes de "em_preparo"
        flash("Este pedido não pode mais ser cancelado.", "erro")
        return redirect(url_for("pedido.acompanhar", pedido_id=pedido.id))

    pedido.status = "cancelado"
    db.session.commit()
    flash(f"Pedido #{pedido.id} cancelado.", "sucesso")
    return redirect(url_for("pedido.meus_pedidos"))
