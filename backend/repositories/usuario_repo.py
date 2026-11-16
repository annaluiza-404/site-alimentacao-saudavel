from repositories.base_repo import executar

COLUNAS = 'id, nome, tipo'


def obter_por_id(usuario_id, cur=None):
    return executar('SELECT id, nome, email, cpf, preferencia, admin '
                    'FROM usuarios WHERE id = %s', (usuario_id,), one=True, cur=cur)


def obter_por_email(email, cur=None):
    return executar('SELECT id, nome, email, cpf, senha, preferencia, admin '
                    'FROM usuarios WHERE email = %s', (email,), one=True, cur=cur)


def email_existe(email, cur=None):
    return executar('SELECT 1 FROM usuarios WHERE email = %s', (email,), one=True, cur=cur)


def inserir(nome, email, senha_hash, preferencia=None, cur=None):
    return executar('INSERT INTO usuarios (nome, email, senha, preferencia) '
                    'VALUES (%s, %s, %s, %s) '
                    'RETURNING id, nome, email, cpf, preferencia, admin',
                    (nome, email, senha_hash, preferencia), one=True, cur=cur)


def cpf_existe(cpf, exceto_id=None, cur=None):
    if exceto_id:
        return executar('SELECT 1 FROM usuarios WHERE cpf = %s AND id <> %s',
                        (cpf, exceto_id), one=True, cur=cur)
    return executar('SELECT 1 FROM usuarios WHERE cpf = %s', (cpf,), one=True, cur=cur)


def atualizar(usuario_id, campos, cur=None):
    colunas = ', '.join(f'{campo} = %s' for campo in campos)
    params = list(campos.values()) + [usuario_id]
    return executar(f'UPDATE usuarios SET {colunas} WHERE id = %s '
                    f'RETURNING id, nome, email, cpf, preferencia, admin',
                    params, one=True, cur=cur)
