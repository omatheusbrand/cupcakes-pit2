"""Testes do carrinho: US-07 (adicionar), US-08 (alterar/remover)."""


def test_adicionar_ao_carrinho(client):
    resposta = client.post("/carrinho/adicionar/1", data={"quantidade": "2"}, follow_redirects=True)
    assert resposta.status_code == 200
    assert b"Baunilha Cl\xc3\xa1ssico" in resposta.data
    assert "R$ 19,00".encode() in resposta.data or "R$ 19.00".encode() in resposta.data


def test_adicionar_duas_vezes_soma_quantidade(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": "2"})
    client.post("/carrinho/adicionar/1", data={"quantidade": "1"})
    resposta = client.get("/carrinho")
    # 3 unidades de R$ 9,50 = R$ 28,50
    assert "R$ 28,50".encode() in resposta.data or "R$ 28.50".encode() in resposta.data


def test_nao_adiciona_cupcake_sem_estoque(client):
    resposta = client.post("/carrinho/adicionar/2", follow_redirects=True)  # id 2 = Esgotado Teste
    assert "indispon\u00edvel".encode() in resposta.data


def test_carrinho_vazio_mostra_mensagem(client):
    resposta = client.get("/carrinho")
    assert "carrinho est\u00e1 vazio".encode() in resposta.data


def test_atualizar_quantidade_recalcula_subtotal(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": "1"})
    client.post("/carrinho/atualizar/1", data={"quantidade": "4"})
    resposta = client.get("/carrinho")
    # 4 x R$ 9,50 = R$ 38,00
    assert "R$ 38,00".encode() in resposta.data or "R$ 38.00".encode() in resposta.data


def test_remover_item_do_carrinho(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": "1"})
    client.post("/carrinho/remover/1")
    resposta = client.get("/carrinho")
    assert "carrinho est\u00e1 vazio".encode() in resposta.data


def test_quantidade_maxima_e_20(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": "25"})
    resposta = client.get("/carrinho")
    # 20 x R$ 9,50 = R$ 190,00
    assert "R$ 190,00".encode() in resposta.data or "R$ 190.00".encode() in resposta.data
