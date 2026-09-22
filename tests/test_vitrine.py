"""Testes da vitrine: US-04 (ver vitrine), US-05 (buscar/filtrar), US-06 (detalhes)."""


def test_vitrine_mostra_cupcakes_ativos(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert b"Baunilha Cl\xc3\xa1ssico" in resposta.data


def test_vitrine_marca_cupcake_sem_estoque_como_esgotado(client):
    resposta = client.get("/")
    assert b"Esgotado" in resposta.data


def test_busca_por_nome_filtra_resultado(client):
    resposta = client.get("/?busca=Baunilha")
    assert b"Baunilha Cl\xc3\xa1ssico" in resposta.data
    assert b"Esgotado Teste" not in resposta.data


def test_busca_sem_resultado_mostra_mensagem(client):
    resposta = client.get("/?busca=NaoExiste")
    assert "Nenhum cupcake encontrado".encode("utf-8") in resposta.data


def test_detalhes_de_cupcake_existente(client):
    resposta = client.get("/cupcake/1")
    assert resposta.status_code == 200
    assert b"Ingredientes" in resposta.data


def test_detalhes_de_cupcake_inexistente_retorna_404(client):
    resposta = client.get("/cupcake/9999")
    assert resposta.status_code == 404
