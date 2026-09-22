# Como rodar o projeto no seu computador (Windows)

1. Copie `.env.example` para um novo arquivo chamado `.env`.
2. Abra o `.env` e cole a connection string do Neon em `DATABASE_URL`
   (aquela que começa com `postgresql://`).
3. Em `SECRET_KEY`, coloque qualquer texto aleatório, por exemplo `abc123troque456`.
4. No PowerShell, dentro da pasta do projeto:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

5. Abra o navegador em http://127.0.0.1:5000

Para rodar os testes automatizados:

```
python -m pytest -v
```

Os testes usam um banco de dados temporário na memória, então não mexem
no seu banco de dados real do Neon.
