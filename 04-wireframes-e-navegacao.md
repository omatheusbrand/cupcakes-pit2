# Interface (IHC): telas, mapa navegacional e mapa conceitual

**Projeto Integrador Transdisciplinar em Engenharia de Software II**
Os wireframes estão em `docs/wireframes.html` e o **protótipo clicável** (navegação entre as telas) em `docs/prototipo.html`. Ambos abrem no navegador. Nome provisório da loja: **Doce Mimo Cupcakes**.

---

## 1. Lista de telas

| ID | Tela | Histórias | Observações de IHC |
|---|---|---|---|
| T01 | Vitrine | US-04, US-05 | Cupcake sem estoque aparece "Esgotado" e sem botão de compra |
| T02 | Detalhes do cupcake | US-06, US-07 | Mostra alergênicos; quantidade de 1 a 20 |
| T03 | Carrinho | US-07, US-08, US-10 | Subtotal recalculado a cada mudança; ✕ remove o item |
| T04 | Login | US-02 | Erro de credenciais em mensagem clara (E01) |
| T05 | Cadastro | US-01 | Indica o mínimo de 8 caracteres na senha |
| T06 | Entrega ou retirada | US-09, US-10 | Retirada não exige endereço nem cobra taxa |
| T07 | Resumo do pedido | US-10, US-11 | Mostra subtotal, taxa e total antes de pagar |
| T08 | Pagamento | US-12 | Pix (código simulado) ou cartão |
| T09 | Confirmação | US-13 | Número do pedido e resumo |
| T10 | Meus pedidos | US-15 | Do mais recente ao mais antigo |
| T11 | Acompanhar pedido | US-14 | Botão de cancelar só antes de "Em preparo" |
| T12 | Perfil e endereços | US-03 | Vários endereços por cliente |
| T13 | Admin: cupcakes | US-16 | Desativar em vez de apagar |
| T14 | Admin: formulário de cupcake | US-16 | Valida preço maior que zero |
| T15 | Admin: pedidos | US-17 | Filtro por status e atualização direta |
| E01 | Erro: login inválido | US-02 | "E-mail ou senha inválidos" |
| E02 | Erro: carrinho vazio | US-08 | Oferece o caminho de volta à vitrine |
| E03 | Erro: pagamento recusado | US-12 | Permite tentar de novo |
| E04 | Erro: item esgotado | US-11 | Diz qual item e o que fazer |
| E05 | Erro: e-mail já cadastrado | US-01 | Sugere entrar na conta |

**Princípios de IHC aplicados:** interface clara e consistente (mesmo cabeçalho em todas as telas), feedback imediato (mensagens de erro e sucesso), ações reversíveis (remover do carrinho, cancelar pedido) e simplicidade (uma tarefa principal por tela).

---

## 2. Mapa navegacional

```mermaid
flowchart TD
  T01["T01 Vitrine"] -->|toca no cupcake| T02["T02 Detalhes"]
  T01 -->|ícone do carrinho| T03["T03 Carrinho"]
  T01 -->|ícone da conta, sem login| T04["T04 Login"]
  T02 -->|adicionar ao carrinho| T03
  T03 -->|carrinho vazio| E02["E02 Carrinho vazio"]
  E02 --> T01
  T03 -->|finalizar, sem login| T04
  T03 -->|finalizar, logado| T06["T06 Entrega ou retirada"]
  T04 -->|credenciais erradas| E01["E01 Login inválido"]
  E01 --> T04
  T04 -->|criar conta| T05["T05 Cadastro"]
  T05 -->|e-mail repetido| E05["E05 E-mail já cadastrado"]
  E05 --> T05
  T05 -->|cadastro ok| T01
  T04 -->|login de cliente ok| T01
  T04 -->|login de admin ok| T15["T15 Admin: pedidos"]
  T06 --> T07["T07 Resumo"]
  T07 -->|item esgotado| E04["E04 Item esgotado"]
  E04 --> T03
  T07 --> T08["T08 Pagamento"]
  T08 -->|recusado| E03["E03 Pagamento recusado"]
  E03 --> T08
  T08 -->|aprovado| T09["T09 Confirmação"]
  T09 --> T11["T11 Acompanhar pedido"]
  T01 -->|menu do cliente| T10["T10 Meus pedidos"]
  T10 --> T11
  T01 -->|menu do cliente| T12["T12 Perfil e endereços"]
  T15 <--> T13["T13 Admin: cupcakes"]
  T13 --> T14["T14 Admin: formulário"]
  T14 --> T13
```

Regra de navegação: todas as telas voltam à Vitrine (T01) pelo logotipo, e as telas de erro sempre têm um caminho de volta.

---

## 3. Mapa conceitual

```mermaid
flowchart LR
  L(("Loja de cupcakes")) -->|vende| CP["Cupcakes"]
  CP -->|são organizados em| CAT["Categorias"]
  CL["Cliente"] -->|escolhe| CP
  CL -->|monta| CAR["Carrinho"]
  CAR -->|se transforma em| PED["Pedido"]
  PED -->|é recebido por| REC["Entrega ou retirada"]
  REC -->|na entrega, usa| END["Endereço"]
  PED -->|é quitado com| PAG["Pagamento: Pix ou cartão"]
  PED -->|passa por| ST["Status do pedido"]
  CL -->|acompanha| ST
  ADM["Administrador"] -->|gerencia| CP
  ADM -->|atualiza| ST
```
