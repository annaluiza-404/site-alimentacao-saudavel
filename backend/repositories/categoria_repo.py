from repositories.base_repo import executar

COLUNAS = 'id, nome, tipo'


def listar(tipo=None, cur=None):
    if tipo:
        return executar(f'SELECT {COLUNAS} FROM categorias WHERE tipo = %s ORDER BY nome',
                        (tipo,), cur=cur)
    return executar(f'SELECT {COLUNAS} FROM categorias ORDER BY nome', cur=cur)


def obter(categoria_id, cur=None):
    return executar(f'SELECT {COLUNAS} FROM categorias WHERE id = %s',
                    (categoria_id,), one=True, cur=cur)


def inserir(nome, tipo='produto', cur=None):
    return executar(f'INSERT INTO categorias (nome, tipo) VALUES (%s, %s) '
                    f'RETURNING {COLUNAS}', (nome, tipo), one=True, cur=cur)


def atualizar(categoria_id, nome, cur=None):
    return executar(f'UPDATE categorias SET nome = %s WHERE id = %s '
                    f'RETURNING {COLUNAS}', (nome, categoria_id), one=True, cur=cur)


def excluir(categoria_id, cur=None):
    return executar('DELETE FROM categorias WHERE id = %s RETURNING id',
                    (categoria_id,), one=True, cur=cur)


def nome_existe(nome, exceto_id=None, cur=None):
    if exceto_id:
        return executar('SELECT 1 FROM categorias WHERE nome = %s AND id <> %s',
                        (nome, exceto_id), one=True, cur=cur)
    return executar('SELECT 1 FROM categorias WHERE nome = %s', (nome,), one=True, cur=cur)
