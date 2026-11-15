import db
from utils import security, validators
from utils.erros import ApiErro


def _publico(linha):
    return {
        'id': linha['id'],
        'nome': linha['nome'],
        'email': linha['email'],
        'preferencia': linha['preferencia'],
        'admin': linha['admin']
    }


def registrar(nome, email, senha, preferencia=None):
    if not nome or len(nome.strip()) < 2:
        raise ApiErro('Informe seu nome')
    email = (email or '').strip().lower()
    if not validators.valida_email(email):
        raise ApiErro('E-mail inválido')
    if not validators.valida_senha(senha):
        raise ApiErro('Senha deve ter no mínimo 6 caracteres')
    if db.query('SELECT 1 FROM usuarios WHERE email = %s', (email,), one=True):
        raise ApiErro('E-mail já cadastrado', 409)
    novo = db.query(
        'INSERT INTO usuarios (nome, email, senha, preferencia) VALUES (%s, %s, %s, %s) '
        'RETURNING id, nome, email, preferencia, admin',
        (nome.strip(), email, security.gerar_hash(senha), preferencia or None),
        one=True
    )
    usuario = _publico(novo)
    security.logar_sessao(usuario['id'])
    return usuario


def logar(email, senha):
    email = (email or '').strip().lower()
    linha = db.query('SELECT * FROM usuarios WHERE email = %s', (email,), one=True)
    if linha is None or not security.conferir_senha(senha or '', linha['senha']):
        raise ApiErro('E-mail ou senha incorretos', 401)
    usuario = _publico(linha)
    security.logar_sessao(usuario['id'])
    return usuario


def deslogar():
    security.deslogar_sessao()


def usuario_logado():
    usuario_id = security.usuario_da_sessao()
    if not usuario_id:
        raise ApiErro('Não autenticado', 401)
    linha = db.query(
        'SELECT id, nome, email, preferencia, admin FROM usuarios WHERE id = %s',
        (usuario_id,), one=True
    )
    if linha is None:
        security.deslogar_sessao()
        raise ApiErro('Não autenticado', 401)
    return _publico(linha)
