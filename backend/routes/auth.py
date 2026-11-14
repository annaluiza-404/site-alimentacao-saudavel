from flask import Blueprint, jsonify, request

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/registro', methods=['POST'])
def registrar_usuario():
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "nome": dados.get('nome'),
        "email": dados.get('email'),
        "senha": dados.get('senha'),
        "preferencia": dados.get('preferencia')
    })

@bp_auth.route('/login', methods=['POST'])
def logar_usuario():
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "email": dados.get('email'),
        "senha": dados.get('senha')
    })

@bp_auth.route('/logout', methods=['POST'])
def deslogar_usuario():
    return jsonify({"mensagem": "Logout realizado"})

@bp_auth.route('/me', methods=['GET'])
def coletar_usuario():
    return jsonify({"mensagem": "Rota de coletar usuario"})

@bp_auth.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "usuario_id": id,
        "nome": dados.get('nome'),
        "cpf": dados.get('cpf'),
        "preferencia": dados.get('preferencia')
    })

@bp_auth.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    return jsonify({
        "usuario_id": id,
        "mensagem": "Rota de excluir usuario"
    })
