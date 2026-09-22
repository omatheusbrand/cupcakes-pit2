"""
Controlador da vitrine (Controller, na sigla MVC).
Cobre US-04 (ver vitrine), US-05 (buscar/filtrar), US-06 (detalhes).
O início da área administrativa (US-16) vem no próximo bloco.
"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import Cupcake, Categoria

vitrine_bp = Blueprint("vitrine", __name__)


@vitrine_bp.route("/")
def index():
    termo = request.args.get("busca", "").strip()
    categoria_id = request.args.get("categoria", type=int)

    consulta = Cupcake.query.filter_by(ativo=True)
    if termo:
        consulta = consulta.filter(Cupcake.nome.ilike(f"%{termo}%"))
    if categoria_id:
        consulta = consulta.filter_by(categoria_id=categoria_id)

    cupcakes = consulta.order_by(Cupcake.nome).all()
    categorias = Categoria.query.order_by(Categoria.nome).all()

    return render_template(
        "vitrine.html",
        cupcakes=cupcakes,
        categorias=categorias,
        termo=termo,
        categoria_id=categoria_id,
    )


@vitrine_bp.route("/cupcake/<int:cupcake_id>")
def detalhes(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return render_template("detalhes.html", cupcake=cupcake)


@vitrine_bp.route("/admin/cupcakes")
def admin_cupcakes():
    # Proteção básica: só administrador logado acessa (Curso alternativo Alfa do CU-03/CU-04)
    if session.get("usuario_papel") != "admin":
        return redirect(url_for("vitrine.index"))

    cupcakes = Cupcake.query.order_by(Cupcake.nome).all()
    return render_template("admin_cupcakes.html", cupcakes=cupcakes)
