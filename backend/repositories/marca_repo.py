from repositories.base_repo import executar

COLUNAS = 'id, nome'


def listar(cur=None):
    return executar(f'SELECT {COLUNAS} FROM marcas ORDER BY nome', cur=cur)


def obter(marca_id, cur=None):
    return executar(f'SELECT {COLUNAS} FROM marcas WHERE id = %s',
                    (marca_id,), one=True, cur=cur)


def inserir(nome, cur=None):
    return executar(f'INSERT INTO marcas (nome) VALUES (%s) RETURNING {COLUNAS}',
                    (nome,), one=True, cur=cur)


def atualizar(marca_id, nome, cur=None):
    return executar(f'UPDATE marcas SET nome = %s WHERE id = %s RETURNING {COLUNAS}',
                    (nome, marca_id), one=True, cur=cur)


def excluir(marca_id, cur=None):
    return executar('DELETE FROM marcas WHERE id = %s RETURNING id',
                    (marca_id,), one=True, cur=cur)


def nome_existe(nome, exceto_id=None, cur=None):
    if exceto_id:
        return executar('SELECT 1 FROM marcas WHERE nome = %s AND id <> %s',
                        (nome, exceto_id), one=True, cur=cur)
    return executar('SELECT 1 FROM marcas WHERE nome = %s', (nome,), one=True, cur=cur)
