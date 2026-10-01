"""Testes do admin: US-16 (gerenciar cupcakes), US-17 (pedidos e status)."""
from werkzeug.security import generate_password_hash
from app import db
from app.models import Usuario, Pedido


def criar_admin_e_logar(client, app):
    with app.app_context():
        admin = Usuario(
            nome="Admin", email="admin@teste.com", telefone="11988887777",
            senha_hash=generate_password_hash("senhaadmin1"), papel="admin",
        )
        db.session.add(admin)
        db.session.commit()
    client.post("/login", data={"email": "admin@teste.com", "senha": "senhaadmin1"})


def criar_cliente_logado(client, email="cliente@teste.com"):
    client.post("/cadastro", data={
        "nome": "Cliente", "email": email, "telefone": "11999990000", "senha": "senha1234",
    })


# --- Curso alternativo Alfa do CU-03/CU-04: acesso restrito ---

def test_area_admin_bloqueada_para_visitante(client):
    resposta = client.get("/admin/cupcakes", follow_redirects=True)
    assert "restrito ao administrador".encode() in resposta.data


def test_area_admin_bloqueada_para_cliente_comum(client):
    criar_cliente_logado(client)
    resposta = client.get("/admin/cupcakes", follow_redirects=True)
    assert "restrito ao administrador".encode() in resposta.data


def test_admin_acessa_lista_de_cupcakes(client, app):
    criar_admin_e_logar(client, app)
    resposta = client.get("/admin/cupcakes")
    assert resposta.status_code == 200
    assert "Baunilha Cl\u00e1ssico".encode() in resposta.data


# --- Cadastrar cupcake (CU-04, US-16) ---

def test_cadastrar_cupcake_com_dados_validos(client, app):
    criar_admin_e_logar(client, app)
    resposta = client.post("/admin/cupcakes/novo", data={
        "nome": "Limão Siciliano", "descricao": "Cítrico", "ingredientes": "Farinha, limão",
        "categoria_id": "1", "preco": "12.00", "estoque": "15",
    }, follow_redirects=True)
    assert "cadastrado".encode() in resposta.data
    assert "Lim\u00e3o Siciliano".encode() in resposta.data


def test_cadastrar_cupcake_com_preco_zero_mostra_erro(client, app):
    criar_admin_e_logar(client, app)
    resposta = client.post("/admin/cupcakes/novo", data={
        "nome": "Teste", "descricao": "Teste", "ingredientes": "Teste",
        "categoria_id": "1", "preco": "0", "estoque": "5",
    }, follow_redirects=True)
    assert "maior que zero".encode() in resposta.data


def test_cadastrar_cupcake_sem_nome_mostra_erro(client, app):
    criar_admin_e_logar(client, app)
    resposta = client.post("/admin/cupcakes/novo", data={
        "nome": "", "descricao": "Teste", "ingredientes": "Teste",
        "categoria_id": "1", "preco": "10", "estoque": "5",
    }, follow_redirects=True)
    assert "Preencha todos os campos".encode() in resposta.data


# --- Editar e desativar (US-16) ---

def test_editar_cupcake_atualiza_preco(client, app):
    criar_admin_e_logar(client, app)
    resposta = client.post("/admin/cupcakes/1/editar", data={
        "nome": "Baunilha Clássico", "descricao": "Teste", "ingredientes": "Farinha",
        "categoria_id": "1", "preco": "15.00", "estoque": "10",
    }, follow_redirects=True)
    assert "R$ 15,00".encode() in resposta.data or "R$ 15.00".encode() in resposta.data


def test_desativar_cupcake_some_da_vitrine(client, app):
    criar_admin_e_logar(client, app)
    client.post("/admin/cupcakes/1/alternar-status")
    client.get("/logout")
    resposta = client.get("/")
    assert "Baunilha Cl\u00e1ssico".encode() not in resposta.data


# --- Painel de pedidos (US-17, CU-03) ---

def _criar_pedido_pago(app, usuario_email="cliente@teste.com"):
    with app.app_context():
        usuario = Usuario.query.filter_by(email=usuario_email).first()
        pedido = Pedido(usuario_id=usuario.id, tipo_recebimento="retirada",
                         subtotal=19.0, taxa_entrega=0, total=19.0, status="recebido")
        db.session.add(pedido)
        db.session.commit()
        return pedido.id


def test_admin_avanca_status_do_pedido(client, app):
    criar_cliente_logado(client)
    pedido_id = _criar_pedido_pago(app)
    client.get("/logout")
    criar_admin_e_logar(client, app)

    resposta = client.post(f"/admin/pedidos/{pedido_id}/status", data={"status": "em_preparo"}, follow_redirects=True)
    assert "atualizado".encode() in resposta.data

    with app.app_context():
        assert Pedido.query.get(pedido_id).status == "em_preparo"


def test_pedido_entregue_nao_pode_ser_alterado(client, app):
    criar_cliente_logado(client)
    pedido_id = _criar_pedido_pago(app)
    with app.app_context():
        p = Pedido.query.get(pedido_id)
        p.status = "entregue"
        db.session.commit()
    client.get("/logout")
    criar_admin_e_logar(client, app)

    resposta = client.post(f"/admin/pedidos/{pedido_id}/status", data={"status": "cancelado"}, follow_redirects=True)
    assert "n\u00e3o pode mais ser alterado".encode() in resposta.data
