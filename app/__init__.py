import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def criar_app():
    """Application factory: monta o app Flask, o banco e as rotas (padrão MVC)."""
    app = Flask(__name__)

    # Se DATABASE_URL não estiver definida (ex.: ainda não configurou o .env),
    # caímos em um banco SQLite local só para não travar a aplicação.
    database_url = os.environ.get("DATABASE_URL") or "sqlite:///local.db"
    # O SQLAlchemy exige "postgresql://", mas alguns provedores (como o Neon)
    # às vezes entregam a URL como "postgres://". Corrigimos aqui.
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chave-temporaria-de-desenvolvimento")

    db.init_app(app)

    # Registra os Controladores (Blueprints), cada um cuidando de uma área do sistema
    from app.controllers.vitrine_controller import vitrine_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(vitrine_bp)
    app.register_blueprint(auth_bp)

    return app
