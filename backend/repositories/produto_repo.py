from repositories.base_repo import executar

COLUNAS = 'id, marca_id, nome, descricao, preco, estoque_qtd, imagem_url, destaque, ativo'
VIEW = ('SELECT v.id, v.nome_produto, v.descricao, v.preco, v.estoque_qtd, '
        'v.nome_marca, v.imagem_url, v.destaque, '
        '(SELECT string_agg(c.nome, \'|\' ORDER BY c.nome) FROM produto_categoria pc '
        'JOIN categorias c ON c.id = pc.categoria_id '
        'WHERE pc.produto_id = v.id) AS categorias '
        'FROM vw_catalogo_disponivel v')


def listar(filtros, cur=None):
    where, params = [], []
    if filtros.get('q'):
        where.append('unaccent(v.nome_produto) ILIKE unaccent(%s)')
        params.append(f"%{filtros['q']}%")
    if filtros.get('marca'):
        where.append('v.nome_marca ILIKE %s')
        params.append(f"%{filtros['marca']}%")
    if filtros.get('cat'):
        where.append('EXISTS (SELECT 1 FROM produto_categoria pc '
                     'WHERE pc.produto_id = v.id AND pc.categoria_id = %s)')
        params.append(filtros['cat'])
    if filtros.get('pr_max'):
        where.append('v.preco <= %s')
        params.append(filtros['pr_max'])
    if filtros.get('destaque'):
        where.append('v.destaque = TRUE')
    if filtros.get('tags'):
        where.append('(SELECT COUNT(*) FROM produto_categoria pc '
                     'JOIN categorias c ON c.id = pc.categoria_id '
                     'WHERE pc.produto_id = v.id AND c.nome = ANY(%s)) = %s')
        params.append(list(filtros['tags']))
        params.append(len(filtros['tags']))
    ordem = {'asc': 'v.preco ASC', 'desc': 'v.preco DESC',
             'az': 'v.nome_produto ASC'}.get(filtros.get('ord'), 'v.id ASC')
    sql = VIEW
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += f' ORDER BY {ordem}'
    return executar(sql, tuple(params), cur=cur)


def obter_ativo(produto_id, cur=None):
    return executar(f'{VIEW} WHERE v.id = %s', (produto_id,), one=True, cur=cur)


def obter(produto_id, cur=None):
    return executar(f'SELECT {COLUNAS} FROM produtos WHERE id = %s',
                    (produto_id,), one=True, cur=cur)


def inserir(dados, cur=None):
    return executar(
        'INSERT INTO produtos (marca_id, nome, descricao, preco, estoque_qtd, '
        'imagem_url, destaque) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING ' + COLUNAS,
        (dados['marca_id'], dados['nome'], dados.get('descricao'),
         dados['preco'], dados['estoque_qtd'], dados.get('imagem_url'),
         dados.get('destaque', False)), one=True, cur=cur)


def atualizar(produto_id, dados, cur=None):
    return executar(
        'UPDATE produtos SET marca_id = %s, nome = %s, descricao = %s, '
        'preco = %s, destaque = %s WHERE id = %s RETURNING ' + COLUNAS,
        (dados['marca_id'], dados['nome'], dados.get('descricao'),
         dados['preco'], dados.get('destaque', False), produto_id),
        one=True, cur=cur)


def ajustar_estoque(produto_id, quantidade, cur=None):
    executar('CALL pr_atualizar_estoque(%s, %s)', (produto_id, quantidade), cur=cur)


def definir_imagem(produto_id, imagem_url, cur=None):
    return executar('UPDATE produtos SET imagem_url = %s WHERE id = %s',
                    (imagem_url, produto_id), one=True, cur=cur)


def desativar(produto_id, cur=None):
    return executar('UPDATE produtos SET ativo = FALSE WHERE id = %s RETURNING id',
                    (produto_id,), one=True, cur=cur)


def vincular_categorias(produto_id, categoria_ids, cur=None):
    for cat_id in categoria_ids:
        executar('INSERT INTO produto_categoria (produto_id, categoria_id) '
                 'VALUES (%s, %s) ON CONFLICT DO NOTHING',
                 (produto_id, cat_id), cur=cur)


def desvincular_todas(produto_id, cur=None):
    executar('DELETE FROM produto_categoria WHERE produto_id = %s',
             (produto_id,), cur=cur)


def categorias_de(produto_id, cur=None):
    return executar('SELECT c.id, c.nome, c.tipo FROM produto_categoria pc '
                    'JOIN categorias c ON c.id = pc.categoria_id '
                    'WHERE pc.produto_id = %s ORDER BY c.id', (produto_id,), cur=cur)


def nome_existe(nome, exceto_id=None, cur=None):
    if exceto_id:
        return executar('SELECT 1 FROM produtos WHERE nome = %s AND id <> %s',
                        (nome, exceto_id), one=True, cur=cur)
    return executar('SELECT 1 FROM produtos WHERE nome = %s', (nome,), one=True, cur=cur)
