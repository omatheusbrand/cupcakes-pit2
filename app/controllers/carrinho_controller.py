"""
Controlador do carrinho (Controller, na sigla MVC).
Cobre US-07 (adicionar ao carrinho) e US-08 (alterar/remover itens).

O carrinho é guardado na sessão do navegador (não no banco) até o pedido
ser finalizado — é só um "rascunho" da compra.
Estrutura: session['carrinho'] = {"3": 2, "1": 1}  (chave = id do cupcake em texto, valor = quantidade)
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Cupcake

carrinho_bp = Blueprint("carrinho", __name__)

QUANTIDADE_MIN = 1
QUANTIDADE_MAX = 20  # RN04


def obter_itens_do_carrinho():
    """Junta o carrinho da sessão com os dados atuais dos cupcakes no banco."""
    carrinho = session.get("carrinho", {})
    itens = []
    for cupcake_id_str, quantidade in carrinho.items():
        cupcake = Cupcake.query.get(int(cupcake_id_str))
        if cupcake:
            itens.append({
                "cupcake": cupcake,
                "quantidade": quantidade,
                "subtotal": cupcake.preco * quantidade,
            })
    return itens


def calcular_subtotal(itens):
    return sum(item["subtotal"] for item in itens)


@carrinho_bp.route("/carrinho")
def ver_carrinho():
    itens = obter_itens_do_carrinho()
    subtotal = calcular_subtotal(itens)
    return render_template("carrinho.html", itens=itens, subtotal=subtotal)


@carrinho_bp.route("/carrinho/adicionar/<int:cupcake_id>", methods=["POST"])
def adicionar(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if not cupcake.disponivel:  # RN10
        flash(f"{cupcake.nome} está indisponível no momento.", "erro")
        return redirect(url_for("vitrine.detalhes", cupcake_id=cupcake_id))

    try:
        quantidade = int(request.form.get("quantidade", 1))
    except ValueError:
        quantidade = 1
    quantidade = max(QUANTIDADE_MIN, min(quantidade, QUANTIDADE_MAX))

    carrinho = session.get("carrinho", {})
    chave = str(cupcake_id)
    nova_quantidade = carrinho.get(chave, 0) + quantidade
    carrinho[chave] = min(nova_quantidade, QUANTIDADE_MAX)  # RN04
    session["carrinho"] = carrinho

    flash(f"{cupcake.nome} adicionado ao carrinho.", "sucesso")
    return redirect(url_for("carrinho.ver_carrinho"))


@carrinho_bp.route("/carrinho/atualizar/<int:cupcake_id>", methods=["POST"])
def atualizar(cupcake_id):
    try:
        quantidade = int(request.form.get("quantidade", 1))
    except ValueError:
        quantidade = 1

    carrinho = session.get("carrinho", {})
    chave = str(cupcake_id)
    if chave in carrinho:
        if quantidade <= 0:
            carrinho.pop(chave)
        else:
            carrinho[chave] = max(QUANTIDADE_MIN, min(quantidade, QUANTIDADE_MAX))  # RN04
        session["carrinho"] = carrinho

    return redirect(url_for("carrinho.ver_carrinho"))


@carrinho_bp.route("/carrinho/remover/<int:cupcake_id>", methods=["POST"])
def remover(cupcake_id):
    carrinho = session.get("carrinho", {})
    carrinho.pop(str(cupcake_id), None)
    session["carrinho"] = carrinho
    return redirect(url_for("carrinho.ver_carrinho"))
