from utils import security, validators
from utils.erros import ApiErro
from services import sessao
from repositories import usuario_repo


def _publico(linha):
    return {
        'id': linha['id'],
        'nome': linha['nome'],
        'email': linha['email'],
        'cpf': linha['cpf'],
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
    if usuario_repo.email_existe(email):
        raise ApiErro('E-mail já cadastrado', 409)
    novo = usuario_repo.inserir(nome.strip(), email,
                                security.gerar_hash(senha), preferencia or None)
    usuario = _publico(novo)
    security.logar_sessao(usuario['id'])
    return usuario


def logar(email, senha):
    email = (email or '').strip().lower()
    linha = usuario_repo.obter_por_email(email)
    if linha is None or not security.conferir_senha(senha or '', linha['senha']):
        raise ApiErro('E-mail ou senha incorretos', 401)
    usuario = _publico(linha)
    security.logar_sessao(usuario['id'])
    return usuario


def deslogar():
    security.deslogar_sessao()


def atualizar_usuario(usuario_id, dados):
    sessao.exigir_dono(usuario_id)
    if usuario_repo.obter_por_id(usuario_id) is None:
        raise ApiErro('Usuário não encontrado', 404)
    campos = {}
    if 'nome' in dados:
        nome = (dados.get('nome') or '').strip()
        if len(nome) < 2:
            raise ApiErro('Informe seu nome')
        if len(nome) > 100:
            raise ApiErro('Nome deve ter no máximo 100 caracteres')
        campos['nome'] = nome
    if 'cpf' in dados:
        cpf = (dados.get('cpf') or '').strip()
        if not cpf:
            campos['cpf'] = None
        else:
            if not validators.valida_cpf(cpf):
                raise ApiErro('CPF inválido')
            cpf = _formatar_cpf(cpf)
            if usuario_repo.cpf_existe(cpf, exceto_id=usuario_id):
                raise ApiErro('CPF já cadastrado para outro usuário', 409)
            campos['cpf'] = cpf
    if 'preferencia' in dados:
        campos['preferencia'] = (dados.get('preferencia') or '').strip() or None
    if dados.get('senha'):
        if not validators.valida_senha(dados.get('senha')):
            raise ApiErro('Senha deve ter no mínimo 6 caracteres')
        campos['senha'] = security.gerar_hash(dados.get('senha'))
    if not campos:
        raise ApiErro('Nada para atualizar')
    return _publico(usuario_repo.atualizar(usuario_id, campos))


def _formatar_cpf(cpf):
    digitos = ''.join(c for c in cpf if c.isdigit())
    return f'{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}'


def usuario_logado():
    usuario_id = security.usuario_da_sessao()
    if not usuario_id:
        raise ApiErro('Não autenticado', 401)
    linha = usuario_repo.obter_por_id(usuario_id)
    if linha is None:
        security.deslogar_sessao()
        raise ApiErro('Não autenticado', 401)
    return _publico(linha)
