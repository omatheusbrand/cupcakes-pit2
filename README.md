# Doce Mimo Cupcakes

Projeto Integrador Transdisciplinar em Engenharia de Software II (Cruzeiro do Sul Virtual).
Aplicativo web de loja de cupcakes: vitrine, carrinho, pedido, pagamento (simulado) e painel administrativo.

## Links

- **Sistema online:** https://cupcakes-pit2.onrender.com/
  > No plano gratuito o serviço "dorme" após ~15 min sem acesso. O primeiro clique
  > depois disso pode levar de 30s a 1 min para responder — é normal, não é falha.
- Protótipo clicável (wireframes): https://omatheusbrand.github.io/cupcakes-pit2/prototipo.html
- Documentação consolidada (PDF): [docs/PIT-II-documentacao-consolidada.pdf](docs/PIT-II-documentacao-consolidada.pdf)

## Estrutura do repositório

- `app/`: código da aplicação (Flask, padrão MVC — models, controllers, templates)
- `tests/`: testes automatizados (pytest)
- `docs/`: documentação de planejamento e modelagem (requisitos ágeis, UML, dados, interface) e protótipo
- `database/`: projeto físico do banco de dados (`schema.sql`, PostgreSQL)

## Tecnologias

Python (Flask) no padrão MVC, PostgreSQL (hospedado no Neon), SQLAlchemy, HTML/CSS,
testes automatizados com pytest, hospedagem no Render.

## Rodando localmente

Veja `README-DEV.md`.

## Status

Vitrine, cadastro e login concluídos e publicados. Carrinho, pedido e pagamento em desenvolvimento.
