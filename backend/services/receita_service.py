import db
from utils.erros import ApiErro
from utils.conversoes import inteiro
from services import sessao
from repositories import receita_repo, produto_repo


def listar(produto_id=None):
    if produto_id:
        inteiro(produto_id, 'produto_id')
        linhas = receita_repo.listar_por_produto(produto_id)
    else:
        linhas = receita_repo.listar()
    return [_formatar(l) for l in linhas]


def detalhar(receita_id):
    linha = receita_repo.obter(inteiro(receita_id, 'receita_id'))
    if linha is None:
        raise ApiErro('Receita não encontrada', 404)
    return _formatar(linha, com_ingredientes=True)


def criar(dados):
    sessao.exigir_admin()
    validos = _dados_validos(dados)
    ingredientes = _ingredientes_validos(dados.get('ingredientes'))
    with db.transacao() as cur:
        linha = receita_repo.inserir(validos, cur=cur)
        receita_repo.inserir_ingredientes(linha['id'], ingredientes, cur=cur)
    return _formatar(linha, com_ingredientes=True)


def atualizar(receita_id, dados):
    sessao.exigir_admin()
    if receita_repo.obter(inteiro(receita_id, 'receita_id')) is None:
        raise ApiErro('Receita não encontrada', 404)
    validos = _dados_validos(dados)
    ingredientes = _ingredientes_validos(dados.get('ingredientes'))
    with db.transacao() as cur:
        linha = receita_repo.atualizar(receita_id, validos, cur=cur)
        if ingredientes is not None:
            receita_repo.trocar_ingredientes(receita_id, ingredientes, cur=cur)
    return _formatar(linha, com_ingredientes=True)


def excluir(receita_id):
    sessao.exigir_admin()
    if receita_repo.obter(inteiro(receita_id, 'receita_id')) is None:
        raise ApiErro('Receita não encontrada', 404)
    receita_repo.excluir(receita_id)
    return {'mensagem': 'Receita excluída'}


def _dados_validos(dados):
    titulo = (dados.get('titulo') or '').strip()
    categoria = (dados.get('categoria') or '').strip()
    texto = (dados.get('texto') or '').strip()
    imagem = (dados.get('imagem') or '').strip()
    if len(titulo) < 3:
        raise ApiErro('Informe o título da receita')
    if len(titulo) > 150:
        raise ApiErro('Título deve ter no máximo 150 caracteres')
    if not categoria:
        raise ApiErro('Informe a categoria da receita')
    if len(categoria) > 50:
        raise ApiErro('Categoria deve ter no máximo 50 caracteres')
    if len(texto) < 20:
        raise ApiErro('O texto da receita deve ter pelo menos 20 caracteres')
    return {'titulo': titulo, 'categoria': categoria,
            'texto': texto, 'imagem': imagem or 'sem-imagem.png'}


def _ingredientes_validos(valor):
    if valor is None or valor == '':
        return None
    if not isinstance(valor, list) or not valor:
        raise ApiErro('Ingredientes deve ser uma lista de {produto_id, quantidade}')
    itens = []
    for item in valor:
        if not isinstance(item, dict):
            raise ApiErro('Formato de ingrediente inválido')
        produto_id = inteiro(item.get('produto_id'), 'ingredientes.produto_id')
        quantidade = (str(item.get('quantidade') or '')).strip()
        if not quantidade:
            raise ApiErro('Informe a quantidade do ingrediente')
        produto = produto_repo.obter(produto_id)
        if produto is None:
            raise ApiErro(f'Produto {produto_id} (ingrediente) não encontrado', 400)
        itens.append({'produto_id': produto_id, 'quantidade': quantidade})
    return itens


def _formatar(linha, com_ingredientes=False):
    receita = {
        'id': linha['id'],
        'titulo': linha['titulo'],
        'categoria': linha['categoria'],
        'texto': linha['texto'],
        'imagem': linha['imagem'],
        'criado_em': str(linha['criado_em'])
    }
    if com_ingredientes:
        receita['ingredientes'] = [
            {'produto_id': i['produto_id'], 'produto': i['produto'],
             'quantidade': i['quantidade']}
            for i in receita_repo.ingredientes_de(linha['id'])]
    return receita

