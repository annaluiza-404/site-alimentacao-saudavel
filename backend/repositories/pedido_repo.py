from repositories.base_repo import executar

COLUNAS = ('id, usuario_id, cupom_id, subtotal, frete, desconto, total, '
           'status, forma_pagamento, cep_entrega, criado_em')


def inserir(dados, cur=None):
    return executar(
        'INSERT INTO pedidos (usuario_id, cupom_id, subtotal, frete, desconto, '
        'total, status, forma_pagamento, cep_entrega) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
        (dados['usuario_id'], dados.get('cupom_id'), dados['subtotal'],
         dados['frete'], dados['desconto'], dados['total'], dados['status'],
         dados['forma_pagamento'], dados['cep_entrega']), one=True, cur=cur)


def inserir_item(pedido_id, produto_id, quantidade, preco_unitario, cur=None):
    return executar(
        'INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) '
        'VALUES (%s, %s, %s, %s) RETURNING id',
        (pedido_id, produto_id, quantidade, preco_unitario), one=True, cur=cur)


def listar(usuario_id=None, cur=None):
    sql = ('SELECT p.id, p.usuario_id, p.cupom_id, p.subtotal, p.frete, '
           'p.desconto, p.total, p.status, p.forma_pagamento, p.cep_entrega, '
           'p.criado_em, u.nome AS usuario_nome '
           'FROM pedidos p JOIN usuarios u ON u.id = p.usuario_id')
    params = ()
    if usuario_id:
        sql += ' WHERE p.usuario_id = %s'
        params = (usuario_id,)
    sql += ' ORDER BY p.criado_em DESC, p.id DESC'
    return executar(sql, params, cur=cur)


def obter(pedido_id, cur=None):
    return executar(f'SELECT {COLUNAS} FROM pedidos WHERE id = %s',
                    (pedido_id,), one=True, cur=cur)


def itens_de(pedido_id, cur=None):
    return executar('SELECT i.id, i.produto_id, p.nome, i.quantidade, '
                    'i.preco_unitario FROM itens_pedido i '
                    'JOIN produtos p ON p.id = i.produto_id '
                    'WHERE i.pedido_id = %s ORDER BY i.id', (pedido_id,), cur=cur)


def atualizar_status(pedido_id, status, cur=None):
    return executar('UPDATE pedidos SET status = %s WHERE id = %s '
                    'RETURNING id, status', (status, pedido_id), one=True, cur=cur)
