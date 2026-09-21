# Especificação Ágil: Aplicativo da Loja de Cupcakes

**Projeto Integrador Transdisciplinar em Engenharia de Software II**
Documentação de planejamento atualizada a partir do PIT I (melhoria contínua / KaiZen).
Versão 1.0

---

## 1. Visão geral

Um cliente possui uma loja de cupcakes gourmet e quer um aplicativo para vender pela internet. O sistema cobre quatro pontos principais: **vitrine virtual**, **pedido eletrônico**, **pagamento** e **entrega**.

### Atores

| Ator | Descrição |
|---|---|
| Visitante | Pessoa sem conta, que só navega pela vitrine |
| Cliente | Pessoa cadastrada e logada, que faz pedidos |
| Administrador | Dono ou funcionário da loja, que gerencia produtos e pedidos |

### Dentro do escopo

Cadastro e login, vitrine com busca, carrinho, escolha de entrega ou retirada, pagamento (Pix e cartão), acompanhamento de pedidos e painel administrativo.

### Fora do escopo (nesta versão)

- Integração real com operadoras de pagamento. O pagamento será **simulado**.
- Cálculo de frete por distância. A taxa de entrega será **fixa**, definida pelo administrador.
- Aplicativo do entregador.

---

## 2. Regras de negócio (RN) e requisitos não funcionais (RNF) globais

**Regras de negócio**

| ID | Regra |
|---|---|
| RN01 | O e-mail do cliente deve ser único no sistema |
| RN02 | A senha deve ter no mínimo 8 caracteres |
| RN03 | O preço de um cupcake deve ser maior que zero |
| RN04 | Um pedido deve ter pelo menos 1 item, com quantidade de 1 a 20 por item |
| RN05 | Para finalizar o pedido, o visitante precisa entrar na conta ou se cadastrar |
| RN06 | Na retirada na loja não há taxa de entrega |
| RN07 | O pedido só é confirmado depois que o pagamento é aprovado |
| RN08 | Status do pedido: Recebido → Em preparo → Saiu para entrega (ou Pronto para retirada) → Entregue. Também existe o status Cancelado |
| RN09 | O cliente só pode cancelar o pedido antes do status "Em preparo" |
| RN10 | Cupcake desativado ou sem estoque não pode ser adicionado ao carrinho |

**Requisitos não funcionais**

| ID | Requisito |
|---|---|
| RNF01 | A interface deve funcionar bem em celular e computador (responsiva) |
| RNF02 | Senhas devem ser armazenadas com criptografia (hash), nunca em texto puro |
| RNF03 | As telas principais devem carregar em até 3 segundos |
| RNF04 | Mensagens de erro devem ser claras e dizer como corrigir o problema |
| RNF05 | Dados pessoais devem ser protegidos e usados só para o funcionamento da loja (LGPD) |

---

## 3. Cartões de história do usuário

> Prioridade: A (mais alta) a E (mais baixa). Pontos de história: escala 1, 2, 3, 5, 8.

### US-01: Cadastrar-me na loja
- **Requerente:** Como visitante
- **Ação:** quero criar uma conta com nome, e-mail, telefone e senha, para poder fazer pedidos.
- **Comentários:** o endereço de entrega é cadastrado depois (US-09).
- **Critérios de aceitação:**
  - CA1: DADO um e-mail não cadastrado, QUANDO envio o formulário válido, ENTÃO a conta é criada e eu entro logado.
  - CA2: DADO um e-mail já cadastrado, QUANDO envio o formulário, ENTÃO vejo a mensagem "E-mail já cadastrado".
- **Regras de negócio:** RN01, RN02
- **Requisitos não funcionais:** RNF02, RNF04
- **Prioridade:** A | **Pontos:** 3

### US-02: Entrar e sair da conta
- **Requerente:** Como cliente cadastrado
- **Ação:** quero fazer login e logout, para acessar meus pedidos com segurança.
- **Comentários:** inclui a opção "esqueci minha senha" apenas como link informativo nesta versão.
- **Critérios de aceitação:**
  - CA1: DADO credenciais corretas, QUANDO faço login, ENTÃO vou para a vitrine com meu nome visível.
  - CA2: DADO credenciais incorretas, QUANDO faço login, ENTÃO vejo "E-mail ou senha inválidos".
  - CA3: DADO que estou logado, QUANDO faço logout, ENTÃO a sessão termina e volto à tela inicial.
- **Regras de negócio:** RN02
- **Requisitos não funcionais:** RNF02, RNF04
- **Prioridade:** A | **Pontos:** 2

### US-03: Editar meu perfil e endereços
- **Requerente:** Como cliente cadastrado
- **Ação:** quero alterar meus dados e gerenciar meus endereços de entrega, para manter tudo atualizado.
- **Comentários:** o cliente pode ter mais de um endereço.
- **Critérios de aceitação:**
  - CA1: DADO que estou logado, QUANDO altero meus dados e salvo, ENTÃO as alterações aparecem no meu perfil.
  - CA2: DADO que estou no perfil, QUANDO adiciono ou removo um endereço, ENTÃO a lista de endereços é atualizada.
- **Regras de negócio:** RN01
- **Requisitos não funcionais:** RNF04, RNF05
- **Prioridade:** C | **Pontos:** 3

### US-04: Ver a vitrine de cupcakes
- **Requerente:** Como visitante ou cliente
- **Ação:** quero ver os cupcakes disponíveis com foto, nome e preço, para escolher o que comprar.
- **Comentários:** é a página inicial do aplicativo.
- **Critérios de aceitação:**
  - CA1: DADO que existem cupcakes ativos, QUANDO abro a página inicial, ENTÃO vejo cartões com foto, nome e preço.
  - CA2: DADO um cupcake sem estoque, QUANDO vejo a vitrine, ENTÃO ele aparece como "Esgotado" e sem botão de compra.
- **Regras de negócio:** RN10
- **Requisitos não funcionais:** RNF01, RNF03
- **Prioridade:** A | **Pontos:** 3

### US-05: Buscar e filtrar cupcakes
- **Requerente:** Como visitante ou cliente
- **Ação:** quero buscar por nome e filtrar por categoria (Tradicionais, Gourmet, Sazonais), para achar mais rápido o que quero.
- **Comentários:** as categorias são cadastradas pelo administrador.
- **Critérios de aceitação:**
  - CA1: DADO que digito parte de um nome, QUANDO busco, ENTÃO vejo só os cupcakes que combinam.
  - CA2: DADO que escolho uma categoria, QUANDO aplico o filtro, ENTÃO vejo só cupcakes daquela categoria.
  - CA3: DADO uma busca sem resultado, QUANDO busco, ENTÃO vejo "Nenhum cupcake encontrado".
- **Regras de negócio:** RN10
- **Requisitos não funcionais:** RNF03, RNF04
- **Prioridade:** B | **Pontos:** 3

### US-06: Ver detalhes de um cupcake
- **Requerente:** Como visitante ou cliente
- **Ação:** quero ver descrição, ingredientes, alergênicos e tamanho, para decidir com segurança.
- **Comentários:** informação de alergênicos é importante em produtos alimentícios.
- **Critérios de aceitação:**
  - CA1: DADO a vitrine, QUANDO clico em um cupcake, ENTÃO vejo a página com descrição, ingredientes, alergênicos e preço.
- **Regras de negócio:** RN10
- **Requisitos não funcionais:** RNF01
- **Prioridade:** B | **Pontos:** 2

### US-07: Adicionar cupcakes ao carrinho
- **Requerente:** Como visitante ou cliente
- **Ação:** quero adicionar cupcakes ao carrinho com a quantidade desejada, para montar meu pedido.
- **Comentários:** o carrinho é mantido durante a navegação.
- **Critérios de aceitação:**
  - CA1: DADO um cupcake disponível, QUANDO clico em "Adicionar", ENTÃO ele aparece no carrinho com a quantidade escolhida.
  - CA2: DADO um cupcake já no carrinho, QUANDO o adiciono de novo, ENTÃO a quantidade é somada.
- **Regras de negócio:** RN04, RN10
- **Requisitos não funcionais:** RNF03
- **Prioridade:** A | **Pontos:** 3

### US-08: Alterar ou remover itens do carrinho
- **Requerente:** Como cliente
- **Ação:** quero mudar a quantidade ou remover itens e ver o subtotal, para ajustar o pedido antes de pagar.
- **Comentários:** o subtotal é recalculado a cada alteração.
- **Critérios de aceitação:**
  - CA1: DADO um item no carrinho, QUANDO altero a quantidade, ENTÃO o subtotal é recalculado.
  - CA2: DADO um item no carrinho, QUANDO o removo, ENTÃO ele some da lista.
  - CA3: DADO o carrinho vazio, QUANDO tento finalizar, ENTÃO vejo "Seu carrinho está vazio".
- **Regras de negócio:** RN04
- **Requisitos não funcionais:** RNF04
- **Prioridade:** A | **Pontos:** 2

### US-09: Escolher entrega ou retirada
- **Requerente:** Como cliente
- **Ação:** quero escolher entre receber em casa ou retirar na loja e informar o endereço, para definir como vou receber.
- **Comentários:** o cliente escolhe um endereço salvo ou cadastra um novo na hora.
- **Critérios de aceitação:**
  - CA1: DADO que escolho "Entrega", QUANDO seleciono ou cadastro um endereço, ENTÃO o endereço fica no pedido.
  - CA2: DADO que escolho "Retirada", QUANDO continuo, ENTÃO nenhum endereço é exigido.
  - CA3: DADO que escolho "Entrega" sem endereço, QUANDO continuo, ENTÃO vejo "Informe o endereço de entrega".
- **Regras de negócio:** RN05, RN06
- **Requisitos não funcionais:** RNF04, RNF05
- **Prioridade:** A | **Pontos:** 3

### US-10: Ver taxa de entrega e total
- **Requerente:** Como cliente
- **Ação:** quero ver a taxa de entrega e o valor total antes de pagar, para saber quanto vou gastar.
- **Comentários:** a taxa é fixa e definida pelo administrador.
- **Critérios de aceitação:**
  - CA1: DADO entrega escolhida, QUANDO vejo o resumo, ENTÃO o total é subtotal + taxa de entrega.
  - CA2: DADO retirada escolhida, QUANDO vejo o resumo, ENTÃO a taxa é R$ 0,00.
- **Regras de negócio:** RN06
- **Requisitos não funcionais:** RNF04
- **Prioridade:** B | **Pontos:** 3

### US-11: Finalizar o pedido
- **Requerente:** Como cliente
- **Ação:** quero revisar o resumo e confirmar o pedido, para seguir ao pagamento.
- **Comentários:** se o visitante não estiver logado, é levado ao login e volta ao carrinho.
- **Critérios de aceitação:**
  - CA1: DADO um carrinho válido e logado, QUANDO confirmo o resumo, ENTÃO sou levado ao pagamento.
  - CA2: DADO um visitante, QUANDO tenta finalizar, ENTÃO é levado ao login e depois volta ao carrinho.
  - CA3: DADO um item que ficou sem estoque, QUANDO confirmo, ENTÃO vejo qual item está indisponível.
- **Regras de negócio:** RN04, RN05, RN10
- **Requisitos não funcionais:** RNF03, RNF04
- **Prioridade:** A | **Pontos:** 5

### US-12: Pagar com Pix ou cartão
- **Requerente:** Como cliente
- **Ação:** quero pagar por Pix ou cartão, para concluir a compra.
- **Comentários:** pagamento simulado nesta versão (sem operadora real).
- **Critérios de aceitação:**
  - CA1: DADO que escolho Pix, QUANDO confirmo, ENTÃO vejo um código de pagamento simulado e o pedido fica aguardando aprovação.
  - CA2: DADO que escolho cartão, QUANDO preencho dados válidos, ENTÃO o pagamento é aprovado e o pedido é confirmado.
  - CA3: DADO dados de cartão inválidos, QUANDO confirmo, ENTÃO vejo o erro e posso tentar de novo.
- **Regras de negócio:** RN07
- **Requisitos não funcionais:** RNF04, RNF05
- **Prioridade:** A | **Pontos:** 5

### US-13: Receber a confirmação do pedido
- **Requerente:** Como cliente
- **Ação:** quero ver uma tela de confirmação com número e resumo do pedido, para ter certeza de que deu certo.
- **Comentários:** o e-mail de confirmação pode ser simulado nesta versão.
- **Critérios de aceitação:**
  - CA1: DADO um pagamento aprovado, QUANDO o pedido é confirmado, ENTÃO vejo o número do pedido, itens, total e forma de recebimento.
- **Regras de negócio:** RN07, RN08
- **Requisitos não funcionais:** RNF04
- **Prioridade:** B | **Pontos:** 2

### US-14: Acompanhar o status do pedido
- **Requerente:** Como cliente
- **Ação:** quero ver em que etapa está meu pedido, para saber quando vai chegar.
- **Comentários:** também permite cancelar antes de "Em preparo".
- **Critérios de aceitação:**
  - CA1: DADO um pedido feito, QUANDO abro o pedido, ENTÃO vejo o status atual.
  - CA2: DADO status anterior a "Em preparo", QUANDO clico em cancelar, ENTÃO o pedido vai para "Cancelado".
  - CA3: DADO status "Em preparo" ou posterior, QUANDO abro o pedido, ENTÃO o botão de cancelar não aparece.
- **Regras de negócio:** RN08, RN09
- **Requisitos não funcionais:** RNF03
- **Prioridade:** B | **Pontos:** 3

### US-15: Ver meu histórico de pedidos
- **Requerente:** Como cliente
- **Ação:** quero ver a lista dos meus pedidos anteriores, para consultar ou repetir uma compra.
- **Comentários:** ordenado do mais recente para o mais antigo.
- **Critérios de aceitação:**
  - CA1: DADO que tenho pedidos, QUANDO abro "Meus pedidos", ENTÃO vejo a lista com número, data, total e status.
  - CA2: DADO que não tenho pedidos, QUANDO abro "Meus pedidos", ENTÃO vejo "Você ainda não fez pedidos".
- **Regras de negócio:** RN08
- **Requisitos não funcionais:** RNF03, RNF05
- **Prioridade:** C | **Pontos:** 2

### US-16: Gerenciar os cupcakes da loja
- **Requerente:** Como administrador
- **Ação:** quero cadastrar, editar e desativar cupcakes (nome, descrição, preço, categoria, foto e estoque), para manter a vitrine atualizada.
- **Comentários:** desativar é melhor que apagar, para não perder o histórico de pedidos.
- **Critérios de aceitação:**
  - CA1: DADO dados válidos, QUANDO cadastro um cupcake, ENTÃO ele aparece na vitrine.
  - CA2: DADO um cupcake existente, QUANDO altero preço ou estoque, ENTÃO a vitrine mostra os novos valores.
  - CA3: DADO um cupcake existente, QUANDO o desativo, ENTÃO ele sai da vitrine.
  - CA4: DADO um preço menor ou igual a zero, QUANDO salvo, ENTÃO vejo uma mensagem de erro.
- **Regras de negócio:** RN03, RN10
- **Requisitos não funcionais:** RNF04
- **Prioridade:** A | **Pontos:** 5

### US-17: Ver pedidos e atualizar o status
- **Requerente:** Como administrador
- **Ação:** quero ver os pedidos recebidos e atualizar o status de cada um, para organizar a produção e a entrega.
- **Comentários:** pedidos novos aparecem primeiro.
- **Critérios de aceitação:**
  - CA1: DADO pedidos confirmados, QUANDO abro o painel, ENTÃO vejo a lista com cliente, itens, total e status.
  - CA2: DADO um pedido, QUANDO avanço o status, ENTÃO o cliente vê o novo status.
  - CA3: DADO um pedido "Entregue" ou "Cancelado", QUANDO tento alterá-lo, ENTÃO o sistema não permite.
- **Regras de negócio:** RN08, RN09
- **Requisitos não funcionais:** RNF03
- **Prioridade:** A | **Pontos:** 5

---

## 4. Mapa de afinidade (agrupamento por tema)

| Tema | Histórias |
|---|---|
| Conta e acesso | US-01, US-02, US-03 |
| Vitrine | US-04, US-05, US-06 |
| Carrinho e pedido | US-07, US-08, US-09, US-10, US-11 |
| Pagamento | US-12, US-13 |
| Acompanhamento | US-14, US-15 |
| Administração | US-16, US-17 |

---

## 5. Backlog de produto priorizado

| Ordem | ID | História do usuário | Pontos | Prioridade |
|---|---|---|---|---|
| 1 | US-04 | Como visitante, quero ver a vitrine de cupcakes | 3 | A |
| 2 | US-16 | Como administrador, quero gerenciar os cupcakes | 5 | A |
| 3 | US-01 | Como visitante, quero me cadastrar | 3 | A |
| 4 | US-02 | Como cliente, quero entrar e sair da conta | 2 | A |
| 5 | US-07 | Como cliente, quero adicionar ao carrinho | 3 | A |
| 6 | US-08 | Como cliente, quero alterar ou remover itens do carrinho | 2 | A |
| 7 | US-09 | Como cliente, quero escolher entrega ou retirada | 3 | A |
| 8 | US-11 | Como cliente, quero finalizar o pedido | 5 | A |
| 9 | US-12 | Como cliente, quero pagar com Pix ou cartão | 5 | A |
| 10 | US-17 | Como administrador, quero ver pedidos e atualizar o status | 5 | A |
| 11 | US-10 | Como cliente, quero ver taxa de entrega e total | 3 | B |
| 12 | US-13 | Como cliente, quero ver a confirmação do pedido | 2 | B |
| 13 | US-14 | Como cliente, quero acompanhar o status do pedido | 3 | B |
| 14 | US-06 | Como visitante, quero ver detalhes de um cupcake | 2 | B |
| 15 | US-05 | Como visitante, quero buscar e filtrar cupcakes | 3 | B |
| 16 | US-15 | Como cliente, quero ver meu histórico de pedidos | 2 | C |
| 17 | US-03 | Como cliente, quero editar perfil e endereços | 3 | C |

**Total:** 17 histórias, 54 pontos.
