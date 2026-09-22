"""Ponto de entrada da aplicação (usado por 'python run.py' e pelo Render)."""
from app import criar_app

app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
