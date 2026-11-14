INSERT INTO categorias (nome, tipo) VALUES
('Pães e massas', 'produto'),
('Doces e biscoitos', 'produto'),
('Snacks', 'produto'),
('Bebidas', 'produto'),
('Mercearia', 'produto'),
('Sem glúten', 'restricao'),
('Sem lactose', 'restricao'),
('Vegano', 'restricao'),
('Sem açúcar', 'restricao'),
('Sem ovo', 'restricao');

INSERT INTO marcas (nome) VALUES
('Intolerância Zero'),
('Grãos & Cia');

INSERT INTO produtos (marca_id, nome, descricao, preco, estoque_qtd, imagem_url, destaque)
SELECT m.id, v.nome, v.descricao, v.preco, v.estoque_qtd, v.imagem_url, v.destaque
FROM (VALUES
('Intolerância Zero', 'Pão de forma de arroz', 'Pão de forma macio, feito com farinha de arroz', 18.90, 30, 'images/produtos/pao-arroz.jpg', TRUE),
('Intolerância Zero', 'Macarrão de milho 500g', 'Massa de milho livre de glúten, cozimento em 8 minutos', 12.50, 40, 'images/produtos/macarrao-milho.jpg', FALSE),
('Intolerância Zero', 'Cookie de aveia sem glúten', 'Cookie crocante de aveia certificada sem glúten', 14.90, 25, 'images/produtos/cookie-aveia.jpg', FALSE),
('Intolerância Zero', 'Brownie de cacau 70%', 'Brownie denso de cacau 70% vegano', 21.00, 20, 'images/produtos/brownie.jpg', TRUE),
('Intolerância Zero', 'Barrinha de castanhas', 'Barrinha de castanhas sem açúcar adicionado', 9.90, 50, 'images/produtos/barrinha-castanhas.jpg', FALSE),
('Intolerância Zero', 'Chips de batata-doce', 'Chips crocante de batata-doce assado', 11.50, 35, 'images/produtos/chips-batata-doce.jpg', FALSE),
('Intolerância Zero', 'Bebida de amêndoas 1L', 'Bebida vegetal de amêndoas sem açúcar', 16.90, 45, 'images/produtos/leite-amendoas.jpg', TRUE),
('Grãos & Cia', 'Kombucha de gengibre', 'Kombucha artesanal de gengibre 500ml', 13.90, 18, 'images/produtos/kombucha-gengibre.jpg', FALSE),
('Grãos & Cia', 'Farinha de arroz integral', 'Farinha de arroz integral para receitas sem glúten', 8.90, 60, 'images/produtos/farinha-arroz.jpg', FALSE),
('Grãos & Cia', 'Pasta de amendoim integral', 'Pasta de amendoim integral sem açúcar', 19.90, 28, 'images/produtos/pasta-amendoim.jpg', FALSE),
('Grãos & Cia', 'Mix de farinhas para bolo', 'Mix pronto de farinhas sem glúten para bolos', 24.90, 22, 'images/produtos/mix-farinhas.jpg', FALSE),
('Grãos & Cia', 'Queijo vegetal de castanhas', 'Queijo vegetal de castanhas maturado 200g', 42.00, 15, 'images/produtos/queijo-castanhas.jpg', TRUE),
('Grãos & Cia', 'Granola sem açúcar', 'Granola sem açúcar com castanhas e sementes 500g', 27.50, 26, 'images/produtos/granola.jpg', FALSE),
('Grãos & Cia', 'Pão de queijo sem lactose', 'Pão de queijo congelado sem lactose 600g', 22.00, 32, 'images/produtos/pao-de-queijo.jpg', FALSE)
) AS v(marca, nome, descricao, preco, estoque_qtd, imagem_url, destaque)
JOIN marcas m ON m.nome = v.marca;

INSERT INTO produto_categoria (produto_id, categoria_id)
SELECT p.id, c.id
FROM (VALUES
('Pão de forma de arroz', 'Pães e massas'),
('Pão de forma de arroz', 'Sem glúten'),
('Pão de forma de arroz', 'Sem lactose'),
('Pão de forma de arroz', 'Vegano'),
('Macarrão de milho 500g', 'Pães e massas'),
('Macarrão de milho 500g', 'Sem glúten'),
('Macarrão de milho 500g', 'Sem lactose'),
('Macarrão de milho 500g', 'Vegano'),
('Macarrão de milho 500g', 'Sem ovo'),
('Cookie de aveia sem glúten', 'Doces e biscoitos'),
('Cookie de aveia sem glúten', 'Sem glúten'),
('Cookie de aveia sem glúten', 'Sem lactose'),
('Brownie de cacau 70%', 'Doces e biscoitos'),
('Brownie de cacau 70%', 'Sem glúten'),
('Brownie de cacau 70%', 'Sem lactose'),
('Brownie de cacau 70%', 'Vegano'),
('Brownie de cacau 70%', 'Sem ovo'),
('Barrinha de castanhas', 'Snacks'),
('Barrinha de castanhas', 'Sem glúten'),
('Barrinha de castanhas', 'Sem lactose'),
('Barrinha de castanhas', 'Vegano'),
('Barrinha de castanhas', 'Sem açúcar'),
('Chips de batata-doce', 'Snacks'),
('Chips de batata-doce', 'Sem glúten'),
('Chips de batata-doce', 'Sem lactose'),
('Chips de batata-doce', 'Vegano'),
('Chips de batata-doce', 'Sem açúcar'),
('Chips de batata-doce', 'Sem ovo'),
('Bebida de amêndoas 1L', 'Bebidas'),
('Bebida de amêndoas 1L', 'Sem glúten'),
('Bebida de amêndoas 1L', 'Sem lactose'),
('Bebida de amêndoas 1L', 'Vegano'),
('Bebida de amêndoas 1L', 'Sem açúcar'),
('Kombucha de gengibre', 'Bebidas'),
('Kombucha de gengibre', 'Sem glúten'),
('Kombucha de gengibre', 'Sem lactose'),
('Kombucha de gengibre', 'Vegano'),
('Farinha de arroz integral', 'Mercearia'),
('Farinha de arroz integral', 'Sem glúten'),
('Farinha de arroz integral', 'Sem lactose'),
('Farinha de arroz integral', 'Vegano'),
('Farinha de arroz integral', 'Sem açúcar'),
('Farinha de arroz integral', 'Sem ovo'),
('Pasta de amendoim integral', 'Mercearia'),
('Pasta de amendoim integral', 'Sem glúten'),
('Pasta de amendoim integral', 'Sem lactose'),
('Pasta de amendoim integral', 'Vegano'),
('Pasta de amendoim integral', 'Sem açúcar'),
('Mix de farinhas para bolo', 'Mercearia'),
('Mix de farinhas para bolo', 'Sem glúten'),
('Mix de farinhas para bolo', 'Sem lactose'),
('Mix de farinhas para bolo', 'Vegano'),
('Queijo vegetal de castanhas', 'Mercearia'),
('Queijo vegetal de castanhas', 'Sem glúten'),
('Queijo vegetal de castanhas', 'Sem lactose'),
('Queijo vegetal de castanhas', 'Vegano'),
('Queijo vegetal de castanhas', 'Sem ovo'),
('Granola sem açúcar', 'Snacks'),
('Granola sem açúcar', 'Sem lactose'),
('Granola sem açúcar', 'Vegano'),
('Granola sem açúcar', 'Sem açúcar'),
('Pão de queijo sem lactose', 'Pães e massas'),
('Pão de queijo sem lactose', 'Sem glúten'),
('Pão de queijo sem lactose', 'Sem lactose')
) AS v(produto, categoria)
JOIN produtos p ON p.nome = v.produto
JOIN categorias c ON c.nome = v.categoria;

INSERT INTO cupons (codigo, valor_desconto, tipo_desconto, minimo_subtotal, data_validade) VALUES
('BEMVINDO10', 10.00, 'percentual', 0, '2026-12-31'),
('FRETEGRATIS', 15.00, 'fixo', 80.00, '2026-12-31'),
('EXPIRADO10', 10.00, 'percentual', 0, '2026-10-31');

INSERT INTO usuarios (nome, email, cpf, senha, preferencia, admin) VALUES
('Admin Intolerância Zero', 'admin@intoleranciazero.com', '529.982.247-76', 'admin123', NULL, TRUE),
('Maria Silva', 'maria@email.com', NULL, 'maria123', 'Sem lactose', FALSE);

INSERT INTO enderecos (usuario_id, cep, logradouro, numero, complemento, bairro, cidade, estado)
SELECT u.id, v.cep, v.logradouro, v.numero, v.complemento, v.bairro, v.cidade, v.estado
FROM (VALUES
('maria@email.com', '01001-000', 'Praça da Sé', '100', 'Apto 42', 'Centro', 'São Paulo', 'SP')
) AS v(email, cep, logradouro, numero, complemento, bairro, cidade, estado)
JOIN usuarios u ON u.email = v.email;

DO $$
BEGIN
    ALTER TABLE itens_pedido DISABLE TRIGGER trg_baixa_estoque_pedido;
EXCEPTION
    WHEN undefined_object THEN NULL;
END $$;

DO $$
DECLARE
    id_maria       BIGINT;
    id_cupom       BIGINT;
    id_pao         BIGINT;
    id_farinha     BIGINT;
    id_barrinha    BIGINT;
    id_kombucha    BIGINT;
    pedido_pago    BIGINT;
    pedido_cancel  BIGINT;
    pedido_pend    BIGINT;
BEGIN
    SELECT id INTO id_maria    FROM usuarios WHERE email = 'maria@email.com';
    SELECT id INTO id_cupom    FROM cupons   WHERE codigo = 'BEMVINDO10';
    SELECT id INTO id_pao      FROM produtos WHERE nome = 'Pão de forma de arroz';
    SELECT id INTO id_farinha  FROM produtos WHERE nome = 'Farinha de arroz integral';
    SELECT id INTO id_barrinha FROM produtos WHERE nome = 'Barrinha de castanhas';
    SELECT id INTO id_kombucha FROM produtos WHERE nome = 'Kombucha de gengibre';

    INSERT INTO pedidos (usuario_id, cupom_id, subtotal, frete, desconto, total, status, forma_pagamento, cep_entrega)
    VALUES (id_maria, id_cupom, 46.70, 12.50, 4.67, 54.53, 'pago', 'pix', '01001-000')
    RETURNING id INTO pedido_pago;

    INSERT INTO pedidos (usuario_id, subtotal, frete, desconto, total, status, forma_pagamento, cep_entrega)
    VALUES (id_maria, 29.70, 10.00, 0, 39.70, 'cancelado', 'boleto', '01001-000')
    RETURNING id INTO pedido_cancel;

    INSERT INTO pedidos (usuario_id, subtotal, frete, desconto, total, status, forma_pagamento, cep_entrega)
    VALUES (id_maria, 13.90, 10.00, 0, 23.90, 'pendente', 'cartao', '01001-000')
    RETURNING id INTO pedido_pend;

    INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES
    (pedido_pago,   id_pao,      2, 18.90),
    (pedido_pago,   id_farinha,  1, 8.90),
    (pedido_cancel, id_barrinha, 3, 9.90),
    (pedido_pend,   id_kombucha, 1, 13.90);
END $$;

DO $$
BEGIN
    ALTER TABLE itens_pedido ENABLE TRIGGER trg_baixa_estoque_pedido;
EXCEPTION
    WHEN undefined_object THEN NULL;
END $$;

INSERT INTO receitas (titulo, categoria, texto, imagem) VALUES
('5 cafés da manhã sem glúten e sem lactose', 'Receitas', 'Panqueca de banana com aveia certificada, tapioca recheada, mingau de arroz com canela, torradas de pão de arroz com pasta de amendoim e vitamina de bebida vegetal. Todas ficam prontas em menos de 15 minutos.', 'images/blog/cafe-manha.jpg'),
('Granola crocante com pasta de amendoim', 'Receitas', 'Misture a granola sem açúcar com a pasta de amendoim e leve ao forno por 10 minutos para ficar crocante. Sirva com bebida vegetal gelada.', 'images/blog/despensa.jpg');

INSERT INTO ingrediente_receita (receita_id, produto_id, quantidade)
SELECT r.id, p.id, v.quantidade
FROM (VALUES
('5 cafés da manhã sem glúten e sem lactose', 'Farinha de arroz integral', '1 xícara'),
('5 cafés da manhã sem glúten e sem lactose', 'Bebida de amêndoas 1L', '1 copo'),
('5 cafés da manhã sem glúten e sem lactose', 'Pão de forma de arroz', '2 fatias'),
('Granola crocante com pasta de amendoim', 'Granola sem açúcar', '2 xícaras'),
('Granola crocante com pasta de amendoim', 'Pasta de amendoim integral', '1 colher de sopa')
) AS v(receita, produto, quantidade)
JOIN receitas r ON r.titulo = v.receita
JOIN produtos p ON p.nome = v.produto;
