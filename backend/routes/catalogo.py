from flask import Blueprint, jsonify, request

from services import produto_service
from utils.imagens import salvar_imagem, ErroImagem
from utils.erros import ApiErro

bp_catalogo = Blueprint('catalogo', __name__)


@bp_catalogo.route('/produtos', methods=['GET'])
def coletar_produtos():
    a = request.args
    produtos = produto_service.listar(
        a.get('q'), a.get('tags'), a.get('cat'), a.get('pr_max'),
        a.get('ord'), a.get('marca'), a.get('destaque'))
    return jsonify({'produtos': produtos})


@bp_catalogo.route('/produtos/<int:id>', methods=['GET'])
def coletar_produto(id):
    return jsonify({'produto': produto_service.detalhar(id)})


@bp_catalogo.route('/produtos/destaques', methods=['GET'])
def coletar_produtos_destaques():
    return jsonify({'produtos': produto_service.listar_destaques()})


@bp_catalogo.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.form
    imagem = _imagem(request)
    return jsonify({'produto': produto_service.criar(dados, imagem)}), 201


@bp_catalogo.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.form
    imagem = _imagem(request)
    return jsonify({'produto': produto_service.atualizar(id, dados, imagem)})


@bp_catalogo.route('/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    return jsonify(produto_service.excluir(id))


@bp_catalogo.route('/categorias', methods=['GET'])
def coletar_categorias():
    return jsonify({'categorias': produto_service.listar_categorias()})


@bp_catalogo.route('/categorias', methods=['POST'])
def criar_categoria():
    dados = request.get_json(silent=True) or {}
    return jsonify({'categoria': produto_service.criar_categoria(dados)}), 201


@bp_catalogo.route('/categorias/<int:id>', methods=['PUT'])
def atualizar_categoria(id):
    dados = request.get_json(silent=True) or {}
    return jsonify({'categoria': produto_service.atualizar_categoria(id, dados)})


@bp_catalogo.route('/categorias/<int:id>', methods=['DELETE'])
def excluir_categoria(id):
    return jsonify(produto_service.excluir_categoria(id))


@bp_catalogo.route('/marcas', methods=['GET'])
def coletar_marcas():
    return jsonify({'marcas': produto_service.listar_marcas()})


@bp_catalogo.route('/marcas', methods=['POST'])
def criar_marca():
    dados = request.get_json(silent=True) or {}
    return jsonify({'marca': produto_service.criar_marca(dados)}), 201


@bp_catalogo.route('/marcas/<int:id>', methods=['PUT'])
def atualizar_marca(id):
    dados = request.get_json(silent=True) or {}
    return jsonify({'marca': produto_service.atualizar_marca(id, dados)})


@bp_catalogo.route('/marcas/<int:id>', methods=['DELETE'])
def excluir_marca(id):
    return jsonify(produto_service.excluir_marca(id))


def _imagem(request):
    try:
        return salvar_imagem(request.files.get('imagem'))
    except ErroImagem as e:
        raise ApiErro(str(e), 400)
