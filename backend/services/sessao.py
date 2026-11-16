from flask import session

from utils.erros import ApiErro
from repositories import usuario_repo


def exigir_logado():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        raise ApiErro('Não autenticado', 401)
    return usuario_id


def exigir_admin():
    usuario = usuario_repo.obter_por_id(exigir_logado())
    if usuario is None:
        raise ApiErro('Não autenticado', 401)
    if not usuario['admin']:
        raise ApiErro('Acesso restrito a administradores', 403)
    return usuario['id']


def exigir_dono(usuario_id):
    usuario = usuario_repo.obter_por_id(exigir_logado())
    if usuario is None:
        raise ApiErro('Não autenticado', 401)
    if not usuario['admin'] and usuario['id'] != usuario_id:
        raise ApiErro('Você não tem permissão sobre este recurso', 403)
