import bcrypt
from flask import session


def gerar_hash(senha):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def conferir_senha(senha, senha_hash):
    try:
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))
    except (ValueError, TypeError):
        return False


def logar_sessao(usuario_id):
    session['usuario_id'] = usuario_id


def deslogar_sessao():
    session.clear()


def usuario_da_sessao():
    return session.get('usuario_id')
