from flask import Blueprint, jsonify, request

bp_catalogo = Blueprint('catalogo', __name__)

@bp_catalogo.route('/produtos', methods=['GET'])
def coletar_produtos():
    q = request.args.get('q')
    tags = request.args.get('tags')
    cat = request.args.get('cat')
    pr_max = request.args.get('pr_max')
    ordem = request.args.get('ord')

    return jsonify({
        "q": q,
        "tags": tags,
        "cat": cat,
        "pr_max": pr_max,
        "ord": ordem
    })

@bp_catalogo.route('/produtos/destaques', methods=['GET'])
def coletar_produtos_destaques():
    return jsonify({"mensagem": "Rota de produtos destaques"})
