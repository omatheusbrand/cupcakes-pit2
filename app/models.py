"""
Modelos (Model, na sigla MVC).
Cada classe aqui representa uma tabela do banco (ver database/schema.sql).
Usamos o SQLAlchemy: ele traduz os comandos Python em SQL por trás dos panos.
"""
from datetime import datetime
from app import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    papel = db.Column(db.String(10), nullable=False, default="cliente")  # 'cliente' ou 'admin'
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    enderecos = db.relationship("Endereco", backref="usuario", lazy=True)

    @property
    def is_admin(self):
        return self.papel == "admin"


class Endereco(db.Model):
    __tablename__ = "endereco"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    rua = db.Column(db.String(120), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(60))
    bairro = db.Column(db.String(60), nullable=False)
    cidade = db.Column(db.String(60), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(8), nullable=False)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.uf}"


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)


class Cupcake(db.Model):
    __tablename__ = "cupcake"

    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    ingredientes = db.Column(db.String(300), nullable=False)
    alergenicos = db.Column(db.String(150))
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    foto_url = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    categoria = db.relationship("Categoria")

    @property
    def disponivel(self):
        return self.ativo and self.estoque > 0


class Configuracao(db.Model):
    __tablename__ = "configuracao"

    id = db.Column(db.SmallInteger, primary_key=True, default=1)
    taxa_entrega = db.Column(db.Numeric(10, 2), nullable=False, default=8.00)
