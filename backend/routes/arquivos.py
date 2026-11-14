from flask import Blueprint, send_from_directory

from utils.imagens import PASTA_UPLOADS

bp_arquivos = Blueprint('arquivos', __name__)


@bp_arquivos.route('/uploads/<path:caminho>', methods=['GET'])
def servir_upload(caminho):
    return send_from_directory(PASTA_UPLOADS, caminho)
