"""Testes de conta: US-01 (cadastro), US-02 (login/logout)."""


def cadastrar(client, email="maria@teste.com", senha="senha1234"):
    return client.post("/cadastro", data={
        "nome": "Maria", "email": email, "telefone": "11999990000", "senha": senha,
    }, follow_redirects=True)


def test_cadastro_com_dados_validos_entra_logado(client):
    resposta = cadastrar(client)
    assert resposta.status_code == 200
    assert "Bem-vindo(a), Maria!".encode("utf-8") in resposta.data


def test_cadastro_com_senha_curta_mostra_erro(client):
    resposta = client.post("/cadastro", data={
        "nome": "Maria", "email": "maria@teste.com", "telefone": "11999990000", "senha": "123",
    }, follow_redirects=True)
    assert "no m\u00ednimo 8 caracteres".encode("utf-8") in resposta.data


def test_cadastro_com_email_repetido_mostra_erro(client):
    cadastrar(client, email="repetido@teste.com")
    client.get("/logout")
    resposta = cadastrar(client, email="repetido@teste.com")
    assert "j\u00e1 cadastrado".encode("utf-8") in resposta.data


def test_login_com_credenciais_corretas(client):
    cadastrar(client, email="joao@teste.com", senha="minhasenha1")
    client.get("/logout")
    resposta = client.post("/login", data={
        "email": "joao@teste.com", "senha": "minhasenha1",
    }, follow_redirects=True)
    assert "Ol\u00e1, Maria".encode("utf-8") in resposta.data


def test_login_com_senha_errada_mostra_erro(client):
    cadastrar(client, email="joao@teste.com", senha="minhasenha1")
    client.get("/logout")
    resposta = client.post("/login", data={
        "email": "joao@teste.com", "senha": "senhaerrada",
    }, follow_redirects=True)
    assert "inv\u00e1lidos".encode("utf-8") in resposta.data


def test_logout_encerra_sessao(client):
    cadastrar(client)
    resposta = client.get("/logout", follow_redirects=True)
    assert "Entrar".encode("utf-8") in resposta.data
    assert "Ol\u00e1, Maria".encode("utf-8") not in resposta.data
