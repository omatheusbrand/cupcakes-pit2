-- Projeto físico do banco de dados: loja de cupcakes
-- SGBD: PostgreSQL

CREATE TABLE usuario (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(120) NOT NULL UNIQUE,
    telefone    VARCHAR(20)  NOT NULL,
    senha_hash  VARCHAR(255) NOT NULL,
    papel       VARCHAR(10)  NOT NULL DEFAULT 'cliente'
                CHECK (papel IN ('cliente', 'admin')),
    criado_em   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE endereco (
    id           SERIAL PRIMARY KEY,
    usuario_id   INTEGER      NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    rua          VARCHAR(120) NOT NULL,
    numero       VARCHAR(10)  NOT NULL,
    complemento  VARCHAR(60),
    bairro       VARCHAR(60)  NOT NULL,
    cidade       VARCHAR(60)  NOT NULL,
    uf           CHAR(2)      NOT NULL,
    cep          CHAR(8)      NOT NULL
);

CREATE TABLE categoria (
    id    SERIAL PRIMARY KEY,
    nome  VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE cupcake (
    id            SERIAL PRIMARY KEY,
    categoria_id  INTEGER       NOT NULL REFERENCES categoria(id),
    nome          VARCHAR(80)   NOT NULL,
    descricao     VARCHAR(300)  NOT NULL,
    ingredientes  VARCHAR(300)  NOT NULL,
    alergenicos   VARCHAR(150),
    preco         NUMERIC(10,2) NOT NULL CHECK (preco > 0),           -- RN03
    estoque       INTEGER       NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    foto_url      VARCHAR(255),
    ativo         BOOLEAN       NOT NULL DEFAULT TRUE
);

-- Linha única com as configurações da loja
CREATE TABLE configuracao (
    id            SMALLINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    taxa_entrega  NUMERIC(10,2) NOT NULL DEFAULT 8.00 CHECK (taxa_entrega >= 0)
);

CREATE TABLE pedido (
    id                SERIAL PRIMARY KEY,
    usuario_id        INTEGER       NOT NULL REFERENCES usuario(id),
    endereco_id       INTEGER       REFERENCES endereco(id) ON DELETE RESTRICT,
    tipo_recebimento  VARCHAR(10)   NOT NULL
                      CHECK (tipo_recebimento IN ('entrega', 'retirada')),
    subtotal          NUMERIC(10,2) NOT NULL CHECK (subtotal >= 0),
    taxa_entrega      NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (taxa_entrega >= 0),
    total             NUMERIC(10,2) NOT NULL CHECK (total >= 0),
    status            VARCHAR(25)   NOT NULL DEFAULT 'aguardando_pagamento'
                      CHECK (status IN ('aguardando_pagamento', 'recebido', 'em_preparo',
                                        'saiu_para_entrega', 'pronto_para_retirada',
                                        'entregue', 'cancelado')),          -- RN08
    criado_em         TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Entrega exige endereço; retirada não (RN06)
    CHECK (tipo_recebimento = 'retirada' OR endereco_id IS NOT NULL)
);

CREATE TABLE item_pedido (
    id              SERIAL PRIMARY KEY,
    pedido_id       INTEGER       NOT NULL REFERENCES pedido(id) ON DELETE CASCADE,
    cupcake_id      INTEGER       NOT NULL REFERENCES cupcake(id),
    quantidade      INTEGER       NOT NULL CHECK (quantidade BETWEEN 1 AND 20),  -- RN04
    preco_unitario  NUMERIC(10,2) NOT NULL CHECK (preco_unitario > 0),
    UNIQUE (pedido_id, cupcake_id)
);

CREATE TABLE pagamento (
    id           SERIAL PRIMARY KEY,
    pedido_id    INTEGER       NOT NULL UNIQUE REFERENCES pedido(id) ON DELETE CASCADE,
    metodo       VARCHAR(10)   NOT NULL CHECK (metodo IN ('pix', 'cartao')),
    status       VARCHAR(10)   NOT NULL DEFAULT 'pendente'
                 CHECK (status IN ('pendente', 'aprovado', 'recusado')),
    valor        NUMERIC(10,2) NOT NULL CHECK (valor > 0),
    codigo_pix   VARCHAR(100),
    cartao_final CHAR(4),        -- só os 4 últimos dígitos; nunca guardar o número completo
    criado_em    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cupcake_categoria ON cupcake(categoria_id);
CREATE INDEX idx_pedido_usuario    ON pedido(usuario_id);
CREATE INDEX idx_item_pedido       ON item_pedido(pedido_id);

-- Dados iniciais (troque pelos sabores da sua loja)
INSERT INTO configuracao (id, taxa_entrega) VALUES (1, 8.00);

INSERT INTO categoria (nome) VALUES ('Tradicionais'), ('Gourmet'), ('Sazonais');

INSERT INTO cupcake (categoria_id, nome, descricao, ingredientes, alergenicos, preco, estoque) VALUES
(1, 'Baunilha Clássico', 'Massa de baunilha com cobertura de buttercream.',
    'Farinha, ovos, manteiga, açúcar, baunilha', 'Glúten, ovos, leite', 9.50, 30),
(1, 'Chocolate Intenso', 'Massa de chocolate com ganache.',
    'Farinha, ovos, cacau, chocolate, manteiga', 'Glúten, ovos, leite', 10.00, 30),
(2, 'Red Velvet', 'Massa aveludada com cream cheese.',
    'Farinha, ovos, cacau, cream cheese, manteiga', 'Glúten, ovos, leite', 13.00, 20),
(3, 'Cenoura com Brigadeiro', 'Cenoura fofinha com brigadeiro.',
    'Farinha, cenoura, ovos, chocolate, leite condensado', 'Glúten, ovos, leite', 11.00, 20);
