CREATE OR REPLACE PROCEDURE pr_atualizar_estoque(
    p_id_produto       BIGINT,
    p_nova_quantidade  INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE produtos
    SET estoque_qtd = p_nova_quantidade
    WHERE id = p_id_produto;

    RAISE NOTICE 'Estoque do produto % atualizado com sucesso!', p_id_produto;
END;
$$;

CREATE OR REPLACE FUNCTION f_produtos_por_marca(p_nome_marca VARCHAR(100))
RETURNS TABLE (
    id_produto    BIGINT,
    nome_produto  VARCHAR(100),
    descricao     VARCHAR(500),
    preco         DECIMAL(10,2),
    estoque_qtd   INTEGER,
    nome_marca    VARCHAR(100)
)
LANGUAGE sql
AS $$
    SELECT p.id, p.nome, p.descricao, p.preco, p.estoque_qtd, m.nome
    FROM produtos p
    INNER JOIN marcas m ON p.marca_id = m.id
    WHERE m.nome ILIKE '%' || p_nome_marca || '%'
      AND p.ativo
$$;

CREATE OR REPLACE FUNCTION trg_fn_baixa_estoque_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF (SELECT estoque_qtd FROM produtos WHERE id = NEW.produto_id) < NEW.quantidade THEN
        RAISE EXCEPTION 'Estoque insuficiente para o produto %', NEW.produto_id;
    END IF;

    UPDATE produtos
    SET estoque_qtd = estoque_qtd - NEW.quantidade
    WHERE id = NEW.produto_id;

    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_baixa_estoque_pedido
AFTER INSERT ON itens_pedido
FOR EACH ROW
EXECUTE FUNCTION trg_fn_baixa_estoque_pedido();

CREATE OR REPLACE VIEW vw_catalogo_disponivel AS
SELECT
    p.id,
    p.nome          AS nome_produto,
    p.descricao,
    p.preco,
    p.estoque_qtd,
    m.nome          AS nome_marca,
    p.imagem_url,
    p.destaque
FROM produtos p
INNER JOIN marcas m ON p.marca_id = m.id
WHERE p.estoque_qtd > 0
  AND p.ativo;
