from flask import Blueprint, jsonify, request

from utils.imagens import salvar_imagem, ErroImagem

bp_catalogo = Blueprint('catalogo', __name__)

@bp_catalogo.route('/produtos', methods=['GET'])
def coletar_produtos():
    q = request.args.get('q')
    tags = request.args.get('tags')
    cat = request.args.get('cat')
    pr_max = request.args.get('pr_max')
    ordem = request.args.get('ord')
    marca = request.args.get('marca')
    destaque = request.args.get('destaque')

    return jsonify({
        "q": q,
        "tags": tags,
        "cat": cat,
        "pr_max": pr_max,
        "ord": ordem,
        "marca": marca,
        "destaque": destaque
    })

@bp_catalogo.route('/produtos/destaques', methods=['GET'])
def coletar_produtos_destaques():
    return jsonify({"mensagem": "Rota de produtos destaques"})

@bp_catalogo.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.form
    try:
        imagem = salvar_imagem(request.files.get('imagem'))
    except ErroImagem as e:
        return jsonify({"erro": str(e)}), 400
    return jsonify({
        "nome": dados.get('nome'),
        "descricao": dados.get('descricao'),
        "preco": dados.get('preco'),
        "estoque": dados.get('estoque'),
        "marca_id": dados.get('marca_id'),
        "categorias": dados.get('categorias'),
        "imagem": imagem,
        "destaque": dados.get('destaque')
    })

@bp_catalogo.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.form
    try:
        imagem = salvar_imagem(request.files.get('imagem'))
    except ErroImagem as e:
        return jsonify({"erro": str(e)}), 400
    return jsonify({
        "produto_id": id,
        "nome": dados.get('nome'),
        "descricao": dados.get('descricao'),
        "preco": dados.get('preco'),
        "estoque": dados.get('estoque'),
        "marca_id": dados.get('marca_id'),
        "categorias": dados.get('categorias'),
        "imagem": imagem,
        "destaque": dados.get('destaque')
    })

@bp_catalogo.route('/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    return jsonify({
        "produto_id": id,
        "mensagem": "Rota de excluir produto"
    })

@bp_catalogo.route('/categorias', methods=['GET'])
def coletar_categorias():
    return jsonify({"mensagem": "Rota de categorias"})

@bp_catalogo.route('/categorias', methods=['POST'])
def criar_categoria():
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "nome": dados.get('nome')
    })

@bp_catalogo.route('/categorias/<int:id>', methods=['PUT'])
def atualizar_categoria(id):
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "categoria_id": id,
        "nome": dados.get('nome')
    })

@bp_catalogo.route('/categorias/<int:id>', methods=['DELETE'])
def excluir_categoria(id):
    return jsonify({
        "categoria_id": id,
        "mensagem": "Rota de excluir categoria"
    })

@bp_catalogo.route('/marcas', methods=['GET'])
def coletar_marcas():
    return jsonify({"mensagem": "Rota de marcas"})

@bp_catalogo.route('/marcas', methods=['POST'])
def criar_marca():
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "nome": dados.get('nome')
    })

@bp_catalogo.route('/marcas/<int:id>', methods=['PUT'])
def atualizar_marca(id):
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "marca_id": id,
        "nome": dados.get('nome')
    })

@bp_catalogo.route('/marcas/<int:id>', methods=['DELETE'])
def excluir_marca(id):
    return jsonify({
        "marca_id": id,
        "mensagem": "Rota de excluir marca"
    })
