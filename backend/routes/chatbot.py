from flask import Blueprint, jsonify, request

from services import chatbot_service

bp_chatbot = Blueprint('chatbot', __name__)


@bp_chatbot.route('/chatbot', methods=['POST'])
def conversar():
    dados = request.get_json(silent=True) or {}
    return jsonify({'resposta': chatbot_service.responder(
        dados.get('pergunta'), dados.get('historico'))})
