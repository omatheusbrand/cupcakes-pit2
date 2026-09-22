"""
Configuração dos testes (pytest).
Usamos um banco SQLite em memória só durante os testes, para não mexer
no banco real (Neon) e para os testes rodarem rápido e de forma isolada.
"""
import os
import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import criar_app, db as _db
from app.models import Categoria, Cupcake


@pytest.fixture
def app():
    app = criar_app()
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    with app.app_context():
        _db.create_all()
        categoria = Categoria(nome="Tradicionais")
        _db.session.add(categoria)
        _db.session.commit()

        _db.session.add(Cupcake(
            categoria_id=categoria.id, nome="Baunilha Clássico",
            descricao="Cupcake de baunilha.", ingredientes="Farinha, ovos, baunilha",
            preco=9.50, estoque=10, ativo=True,
        ))
        _db.session.add(Cupcake(
            categoria_id=categoria.id, nome="Esgotado Teste",
            descricao="Sem estoque.", ingredientes="Farinha",
            preco=8.00, estoque=0, ativo=True,
        ))
        _db.session.commit()

        yield app


@pytest.fixture
def client(app):
    return app.test_client()
