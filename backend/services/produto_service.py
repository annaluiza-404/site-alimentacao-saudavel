import db
from utils.erros import ApiErro
from utils.conversoes import inteiro, decimal, texto_opcional
from services import sessao
from repositories import produto_repo, categoria_repo, marca_repo

ORDEM_VALIDA = ('rel', 'asc', 'desc', 'az')


def listar(q, tags, cat, pr_max, ordem, marca, destaque):
    filtros = {}
    if q and q.strip():
        filtros['q'] = q.strip()
    if marca and marca.strip():
        filtros['marca'] = marca.strip()
    if tags:
        nomes = [t.strip() for t in tags.split(',') if t.strip()]
        if nomes:
            filtros['tags'] = nomes
    if cat is not None and cat != '':
        filtros['cat'] = inteiro(cat, 'cat')
    if pr_max is not None and pr_max != '':
        filtros['pr_max'] = decimal(pr_max, 'pr_max', casas=2)
    if destaque in ('true', '1'):
        filtros['destaque'] = True
    if ordem and ordem not in ORDEM_VALIDA:
        raise ApiErro('Ordenação inválida (use rel, asc, desc ou az)')
    filtros['ord'] = ordem
    return [_formatar(l) for l in produto_repo.listar(filtros)]


def listar_destaques():
    return [_formatar(l) for l in produto_repo.listar({'destaque': True})]


def detalhar(produto_id):
    linha = produto_repo.obter_ativo(produto_id)
    if linha is None:
        raise ApiErro('Produto não encontrado', 404)
    item = _formatar(linha)
    item['categorias'] = [_categoria_formatada(c) for c in produto_repo.categorias_de(produto_id)]
    return item


def criar(dados, imagem_url=None):
    sessao.exigir_admin()
    validos = _dados_validos(dados, imagem_url)
    categorias = _categorias_validas(dados.get('categorias'))
    with db.transacao() as cur:
        linha = produto_repo.inserir(validos, cur=cur)
        produto_repo.vincular_categorias(linha['id'], categorias, cur=cur)
    return detalhar(linha['id'])


def atualizar(produto_id, dados, imagem_url=None):
    sessao.exigir_admin()
    if produto_repo.obter(produto_id) is None:
        raise ApiErro('Produto não encontrado', 404)
    validos = _dados_validos(dados, imagem_url, exceto_id=produto_id)
    categorias = _categorias_validas(dados.get('categorias'))
    with db.transacao() as cur:
        produto_repo.atualizar(produto_id, validos, cur=cur)
        produto_repo.ajustar_estoque(produto_id, validos['estoque_qtd'], cur=cur)
        if imagem_url:
            produto_repo.definir_imagem(produto_id, imagem_url, cur=cur)
        if categorias is not None:
            produto_repo.desvincular_todas(produto_id, cur=cur)
            produto_repo.vincular_categorias(produto_id, categorias, cur=cur)
    return detalhar(produto_id)


def excluir(produto_id):
    sessao.exigir_admin()
    if produto_repo.obter(produto_id) is None:
        raise ApiErro('Produto não encontrado', 404)
    produto_repo.desativar(produto_id)
    return {'mensagem': 'Produto removido do catálogo'}


def listar_categorias():
    return [_categoria_formatada(c) for c in categoria_repo.listar()]


def criar_categoria(dados):
    sessao.exigir_admin()
    nome = (dados.get('nome') or '').strip()
    tipo = dados.get('tipo') or 'produto'
    if len(nome) < 2:
        raise ApiErro('Informe o nome da categoria')
    if len(nome) > 100:
        raise ApiErro('Nome da categoria deve ter no máximo 100 caracteres')
    if tipo not in ('produto', 'restricao'):
        raise ApiErro('Tipo inválido (use produto ou restricao)')
    if categoria_repo.nome_existe(nome):
        raise ApiErro('Categoria já cadastrada', 409)
    return _categoria_formatada(categoria_repo.inserir(nome, tipo))


def atualizar_categoria(categoria_id, dados):
    sessao.exigir_admin()
    if categoria_repo.obter(categoria_id) is None:
        raise ApiErro('Categoria não encontrada', 404)
    nome = (dados.get('nome') or '').strip()
    if len(nome) < 2:
        raise ApiErro('Informe o nome da categoria')
    if len(nome) > 100:
        raise ApiErro('Nome da categoria deve ter no máximo 100 caracteres')
    if categoria_repo.nome_existe(nome, exceto_id=categoria_id):
        raise ApiErro('Categoria já cadastrada', 409)
    return _categoria_formatada(categoria_repo.atualizar(categoria_id, nome))


def excluir_categoria(categoria_id):
    sessao.exigir_admin()
    if categoria_repo.obter(categoria_id) is None:
        raise ApiErro('Categoria não encontrada', 404)
    categoria_repo.excluir(categoria_id)
    return {'mensagem': 'Categoria excluída'}


def listar_marcas():
    return [{'id': m['id'], 'nome': m['nome']} for m in marca_repo.listar()]


def criar_marca(dados):
    sessao.exigir_admin()
    nome = (dados.get('nome') or '').strip()
    if len(nome) < 2:
        raise ApiErro('Informe o nome da marca')
    if len(nome) > 100:
        raise ApiErro('Nome da marca deve ter no máximo 100 caracteres')
    if marca_repo.nome_existe(nome):
        raise ApiErro('Marca já cadastrada', 409)
    linha = marca_repo.inserir(nome)
    return {'id': linha['id'], 'nome': linha['nome']}


def atualizar_marca(marca_id, dados):
    sessao.exigir_admin()
    if marca_repo.obter(marca_id) is None:
        raise ApiErro('Marca não encontrada', 404)
    nome = (dados.get('nome') or '').strip()
    if len(nome) < 2:
        raise ApiErro('Informe o nome da marca')
    if len(nome) > 100:
        raise ApiErro('Nome da marca deve ter no máximo 100 caracteres')
    if marca_repo.nome_existe(nome, exceto_id=marca_id):
        raise ApiErro('Marca já cadastrada', 409)
    linha = marca_repo.atualizar(marca_id, nome)
    return {'id': linha['id'], 'nome': linha['nome']}


def excluir_marca(marca_id):
    sessao.exigir_admin()
    if marca_repo.obter(marca_id) is None:
        raise ApiErro('Marca não encontrada', 404)
    marca_repo.excluir(marca_id)
    return {'mensagem': 'Marca excluída'}


def _dados_validos(dados, imagem_url=None, exceto_id=None):
    nome = (dados.get('nome') or '').strip()
    if len(nome) < 2:
        raise ApiErro('Informe o nome do produto')
    if len(nome) > 100:
        raise ApiErro('Nome do produto deve ter no máximo 100 caracteres')
    if produto_repo.nome_existe(nome, exceto_id=exceto_id):
        raise ApiErro('Produto já cadastrado com esse nome', 409)
    descricao = texto_opcional(dados.get('descricao'))
    if descricao and len(descricao) > 500:
        raise ApiErro('Descrição deve ter no máximo 500 caracteres')
    preco = decimal(dados.get('preco'), 'preco', casas=2)
    if preco < 0:
        raise ApiErro('Preço não pode ser negativo')
    estoque = inteiro(dados.get('estoque'), 'estoque')
    if estoque < 0:
        raise ApiErro('Estoque não pode ser negativo')
    marca_id = inteiro(dados.get('marca_id'), 'marca_id')
    if marca_repo.obter(marca_id) is None:
        raise ApiErro('Marca não encontrada', 400)
    return {
        'nome': nome,
        'descricao': descricao,
        'preco': preco,
        'estoque_qtd': estoque,
        'imagem_url': imagem_url,
        'destaque': dados.get('destaque') in ('true', '1', True),
        'marca_id': marca_id
    }


def _categorias_validas(valor):
    if valor is None or valor == '':
        return None
    if isinstance(valor, str):
        brutos = [c.strip() for c in valor.split(',') if c.strip()]
    else:
        brutos = [str(c).strip() for c in valor]
    ids = []
    for bruto in brutos:
        cat_id = inteiro(bruto, 'categorias')
        if categoria_repo.obter(cat_id) is None:
            raise ApiErro(f'Categoria {cat_id} não encontrada', 400)
        ids.append(cat_id)
    return ids


def _formatar(linha):
    return {
        'id': linha['id'],
        'nome': linha['nome_produto'],
        'descricao': linha['descricao'],
        'preco': float(linha['preco']),
        'estoque': linha['estoque_qtd'],
        'marca': linha['nome_marca'],
        'imagem': linha['imagem_url'],
        'destaque': linha['destaque'],
        'categorias': [n for n in (linha.get('categorias') or '').split('|') if n]
    }


def _categoria_formatada(linha):
    return {'id': linha['id'], 'nome': linha['nome'], 'tipo': linha['tipo']}
