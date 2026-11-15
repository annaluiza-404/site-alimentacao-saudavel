from flask import Blueprint, jsonify, request

from services.auth_service import registrar, logar, deslogar, usuario_logado

bp_auth = Blueprint('auth', __name__)


@bp_auth.route('/registro', methods=['POST'])
def registrar_usuario():
    dados = request.get_json(silent=True) or {}
    return jsonify({'usuario': registrar(
        dados.get('nome'), dados.get('email'),
        dados.get('senha'), dados.get('preferencia')
    )}), 201


@bp_auth.route('/login', methods=['POST'])
def logar_usuario():
    dados = request.get_json(silent=True) or {}
    return jsonify({'usuario': logar(dados.get('email'), dados.get('senha'))})


@bp_auth.route('/logout', methods=['POST'])
def deslogar_usuario():
    deslogar()
    return jsonify({'mensagem': 'Logout realizado'})


@bp_auth.route('/me', methods=['GET'])
def coletar_usuario():
    return jsonify({'usuario': usuario_logado()})
