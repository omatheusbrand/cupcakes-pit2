"""
Controlador de autenticação (Controller, na sigla MVC).
Cobre US-01 (cadastro), US-02 (login/logout).
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        senha = request.form.get("senha", "")

        # RN02: senha com no mínimo 8 caracteres
        if len(senha) < 8:
            flash("A senha deve ter no mínimo 8 caracteres.", "erro")
            return render_template("cadastro.html", nome=nome, email=email, telefone=telefone)

        # RN01: e-mail deve ser único
        if Usuario.query.filter_by(email=email).first():
            flash("E-mail já cadastrado. Tente entrar na sua conta.", "erro")
            return render_template("cadastro.html", nome=nome, email=email, telefone=telefone)

        usuario = Usuario(
            nome=nome,
            email=email,
            telefone=telefone,
            senha_hash=generate_password_hash(senha),  # RNF02: nunca guardamos a senha em texto puro
            papel="cliente",
        )
        db.session.add(usuario)
        db.session.commit()

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        session["usuario_papel"] = usuario.papel
        flash(f"Bem-vindo(a), {usuario.nome}!", "sucesso")
        return redirect(url_for("vitrine.index"))

    return render_template("cadastro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            flash("E-mail ou senha inválidos.", "erro")
            return render_template("login.html", email=email)

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        session["usuario_papel"] = usuario.papel

        if usuario.is_admin:
            return redirect(url_for("vitrine.admin_cupcakes"))
        return redirect(url_for("vitrine.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("vitrine.index"))
