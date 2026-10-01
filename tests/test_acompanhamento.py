"""Testes de acompanhamento: US-14 (status/cancelar), US-15 (histórico)."""
from app import db
from app.models import Pedido, Usuario


def cadastrar_e_logar(client, email="cliente@teste.com"):
    client.post("/cadastro", data={
        "nome": "Cliente", "email": email, "telefone": "11999990000", "senha": "senha1234",
    })


def criar_pedido(app, email, status):
    with app.app_context():
        usuario = Usuario.query.filter_by(email=email).first()
        pedido = Pedido(usuario_id=usuario.id, tipo_recebimento="retirada",
                         subtotal=10.0, taxa_entrega=0, total=10.0, status=status)
        db.session.add(pedido)
        db.session.commit()
        return pedido.id


def test_historico_vazio_mostra_mensagem(client):
    cadastrar_e_logar(client)
    resposta = client.get("/meus-pedidos")
    assert "ainda n\u00e3o fez pedidos".encode() in resposta.data


def test_historico_lista_pedidos_pagos(client, app):
    cadastrar_e_logar(client)
    criar_pedido(app, "cliente@teste.com", "recebido")
    resposta = client.get("/meus-pedidos")
    assert b"#1" in resposta.data


# --- RN09: só cancela antes de "em_preparo" ---

def test_cancelar_pedido_recebido(client, app):
    cadastrar_e_logar(client)
    pedido_id = criar_pedido(app, "cliente@teste.com", "recebido")
    resposta = client.post(f"/pedido/{pedido_id}/cancelar", follow_redirects=True)
    assert "cancelado".encode() in resposta.data
    with app.app_context():
        assert Pedido.query.get(pedido_id).status == "cancelado"


def test_nao_cancela_pedido_em_preparo(client, app):
    cadastrar_e_logar(client)
    pedido_id = criar_pedido(app, "cliente@teste.com", "em_preparo")
    resposta = client.post(f"/pedido/{pedido_id}/cancelar", follow_redirects=True)
    assert "n\u00e3o pode mais ser cancelado".encode() in resposta.data
    with app.app_context():
        assert Pedido.query.get(pedido_id).status == "em_preparo"


def test_botao_cancelar_nao_aparece_em_preparo(client, app):
    cadastrar_e_logar(client)
    pedido_id = criar_pedido(app, "cliente@teste.com", "em_preparo")
    resposta = client.get(f"/pedido/{pedido_id}/acompanhar")
    assert "Cancelar pedido".encode() not in resposta.data


def test_outro_cliente_nao_acessa_pedido_alheio(client, app):
    cadastrar_e_logar(client, email="dono@teste.com")
    pedido_id = criar_pedido(app, "dono@teste.com", "recebido")
    client.get("/logout")
    cadastrar_e_logar(client, email="outro@teste.com")
    resposta = client.get(f"/pedido/{pedido_id}/acompanhar", follow_redirects=True)
    assert "Meus pedidos".encode() in resposta.data
