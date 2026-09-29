"""Testes do pedido e pagamento: US-09 a US-13 (CU-01 e CU-02)."""
import re


def cadastrar_e_logar(client, email="cliente@teste.com"):
    return client.post("/cadastro", data={
        "nome": "Cliente Teste", "email": email, "telefone": "11999990000", "senha": "senha1234",
    }, follow_redirects=True)


def adicionar_item_ao_carrinho(client, cupcake_id=1, quantidade=2):
    client.post(f"/carrinho/adicionar/{cupcake_id}", data={"quantidade": str(quantidade)})


def extrair_pedido_id(resposta_pagamento):
    m = re.search(rb"pedido #(\d+)", resposta_pagamento.data)
    return int(m.group(1)) if m else None


# --- Curso alternativo Alfa do CU-01: exige login ---

def test_finalizar_sem_login_pede_para_entrar(client):
    adicionar_item_ao_carrinho(client)
    resposta = client.get("/pedido/entrega", follow_redirects=True)
    assert "Entrar".encode() in resposta.data
    assert "sua conta".encode() in resposta.data


# --- Curso alternativo Beta do CU-01: carrinho vazio ---

def test_finalizar_com_carrinho_vazio_mostra_erro(client):
    cadastrar_e_logar(client)
    resposta = client.get("/pedido/entrega", follow_redirects=True)
    assert "carrinho est\u00e1 vazio".encode() in resposta.data


# --- Curso alternativo Gama do CU-01: retirada não exige endereço ---

def test_retirada_nao_cobra_taxa(client):
    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client)
    client.post("/pedido/entrega", data={"tipo_recebimento": "retirada"})
    resposta = client.get("/pedido/resumo")
    assert "R$ 0,00".encode() in resposta.data or "R$ 0.00".encode() in resposta.data


def test_entrega_sem_endereco_mostra_erro(client):
    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client)
    resposta = client.post("/pedido/entrega", data={"tipo_recebimento": "entrega"})
    assert "Informe o endere\u00e7o".encode() in resposta.data


def test_novo_endereco_e_usado_no_pedido(client):
    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client)
    client.post("/pedido/endereco/novo", data={
        "rua": "Rua das Flores", "numero": "120", "bairro": "Centro",
        "cidade": "Parnaíba", "uf": "PI", "cep": "64200000",
    }, follow_redirects=True)
    resposta = client.get("/pedido/resumo")
    assert "Rua das Flores".encode() in resposta.data


# --- Resumo com taxa (US-10) ---

def test_resumo_soma_subtotal_e_taxa(client):
    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client, quantidade=2)  # 2 x R$ 9,50 = R$ 19,00
    client.post("/pedido/entrega", data={"tipo_recebimento": "retirada"})
    resposta = client.get("/pedido/resumo")
    assert "R$ 19,00".encode() in resposta.data or "R$ 19.00".encode() in resposta.data


# --- Finalizar pedido cria o registro (US-11) e pagamento aprova (US-12/US-13) ---

def test_fluxo_completo_pix_confirma_pedido(client):
    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client, quantidade=1)
    client.post("/pedido/entrega", data={"tipo_recebimento": "retirada"})
    resposta_pagto = client.post("/pedido/finalizar", follow_redirects=True)
    pedido_id = extrair_pedido_id(resposta_pagto)
    assert pedido_id is not None

    resposta = client.post(f"/pagamento/{pedido_id}/processar", data={"metodo": "pix"}, follow_redirects=True)
    assert "Pedido confirmado".encode() in resposta.data


def test_cartao_com_dados_invalidos_e_recusado(client):
    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client, quantidade=1)
    client.post("/pedido/entrega", data={"tipo_recebimento": "retirada"})
    resposta_pagto = client.post("/pedido/finalizar", follow_redirects=True)
    pedido_id = extrair_pedido_id(resposta_pagto)

    resposta = client.post(f"/pagamento/{pedido_id}/processar", data={
        "metodo": "cartao", "numero_cartao": "123", "validade": "12/30", "cvv": "1",
    }, follow_redirects=True)
    assert "recusado".encode() in resposta.data


def test_cartao_com_dados_validos_aprova_pedido(client):
    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client, quantidade=1)
    client.post("/pedido/entrega", data={"tipo_recebimento": "retirada"})
    resposta_pagto = client.post("/pedido/finalizar", follow_redirects=True)
    pedido_id = extrair_pedido_id(resposta_pagto)

    resposta = client.post(f"/pagamento/{pedido_id}/processar", data={
        "metodo": "cartao", "numero_cartao": "1111222233334444", "validade": "12/30", "cvv": "123",
    }, follow_redirects=True)
    assert "Pedido confirmado".encode() in resposta.data


def test_finalizar_pedido_esvazia_o_carrinho(client):
    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client, quantidade=1)
    client.post("/pedido/entrega", data={"tipo_recebimento": "retirada"})
    client.post("/pedido/finalizar")
    resposta = client.get("/carrinho")
    assert "carrinho est\u00e1 vazio".encode() in resposta.data


def test_finalizar_baixa_estoque_apos_pagamento_aprovado(client, app):
    from app.models import Cupcake

    cadastrar_e_logar(client)
    adicionar_item_ao_carrinho(client, cupcake_id=1, quantidade=3)
    client.post("/pedido/entrega", data={"tipo_recebimento": "retirada"})
    resposta_pagto = client.post("/pedido/finalizar", follow_redirects=True)
    pedido_id = extrair_pedido_id(resposta_pagto)
    client.post(f"/pagamento/{pedido_id}/processar", data={"metodo": "pix"})

    with app.app_context():
        cupcake = Cupcake.query.get(1)
        assert cupcake.estoque == 10 - 3  # estoque inicial (10) menos os 3 comprados
