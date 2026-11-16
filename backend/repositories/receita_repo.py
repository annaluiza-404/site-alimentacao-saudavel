from repositories.base_repo import executar

COLUNAS = 'id, titulo, categoria, texto, imagem, criado_em'


def listar(cur=None):
    return executar(f'SELECT {COLUNAS} FROM receitas ORDER BY criado_em DESC, id DESC',
                    cur=cur)


def listar_por_produto(produto_id, cur=None):
    return executar(
        f'SELECT DISTINCT r.id, r.titulo, r.categoria, r.texto, r.imagem, r.criado_em '
        f'FROM receitas r JOIN ingrediente_receita ir ON ir.receita_id = r.id '
        f'WHERE ir.produto_id = %s ORDER BY r.criado_em DESC, r.id DESC',
        (produto_id,), cur=cur)


def obter(receita_id, cur=None):
    return executar(f'SELECT {COLUNAS} FROM receitas WHERE id = %s',
                    (receita_id,), one=True, cur=cur)


def ingredientes_de(receita_id, cur=None):
    return executar(
        'SELECT ir.produto_id, p.nome AS produto, ir.quantidade '
        'FROM ingrediente_receita ir JOIN produtos p ON p.id = ir.produto_id '
        'WHERE ir.receita_id = %s ORDER BY ir.produto_id', (receita_id,), cur=cur)


def inserir(dados, cur=None):
    return executar(
        'INSERT INTO receitas (titulo, categoria, texto, imagem) '
        'VALUES (%s, %s, %s, %s) RETURNING ' + COLUNAS,
        (dados['titulo'], dados['categoria'], dados['texto'], dados['imagem']),
        one=True, cur=cur)


def inserir_ingredientes(receita_id, itens, cur=None):
    for item in itens:
        executar('INSERT INTO ingrediente_receita (receita_id, produto_id, quantidade) '
                 'VALUES (%s, %s, %s)',
                 (receita_id, item['produto_id'], item['quantidade']), cur=cur)


def trocar_ingredientes(receita_id, itens, cur=None):
    executar('DELETE FROM ingrediente_receita WHERE receita_id = %s',
             (receita_id,), cur=cur)
    inserir_ingredientes(receita_id, itens, cur=cur)


def atualizar(receita_id, dados, cur=None):
    return executar(
        'UPDATE receitas SET titulo = %s, categoria = %s, texto = %s, imagem = %s '
        'WHERE id = %s RETURNING ' + COLUNAS,
        (dados['titulo'], dados['categoria'], dados['texto'], dados['imagem'],
         receita_id), one=True, cur=cur)


def excluir(receita_id, cur=None):
    return executar('DELETE FROM receitas WHERE id = %s RETURNING id',
                    (receita_id,), one=True, cur=cur)
