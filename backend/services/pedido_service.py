import datetime
import db
from utils.erros import ApiErro
from utils import validators
from utils.conversoes import inteiro, decimal, texto_obrigatorio, texto_opcional
from services import sessao
from repositories import (pedido_repo, cupom_repo, endereco_repo,
                          usuario_repo, produto_repo)

FORMAS = ('cartao', 'pix', 'boleto')
STATUSES = ('pendente', 'pago', 'enviado', 'entregue', 'cancelado')
TIPOS_DESCONTO = ('percentual', 'fixo', 'frete')
ZONAS_FRETE = {
    '0': 10.0, '1': 10.0,
    '2': 15.0, '3': 15.0,
    '7': 18.0, '8': 18.0, '9': 18.0,
    '4': 22.0, '5': 22.0, '6': 22.0,
}


def calcular_frete(cep):
    cep = _cep_valido(cep)
    return {'cep': cep, 'valor': ZONAS_FRETE[cep[0]]}


def validar_cupom(codigo, subtotal, frete=0.0):
    linha = cupom_repo.obter_por_codigo(texto_obrigatorio(codigo, 'codigo'))
    if linha is None:
        raise ApiErro('Cupom não encontrado', 404)
    hoje = datetime.date.today()
    if linha['data_validade'] < hoje:
        raise ApiErro('Cupom expirado')
    sub = decimal(subtotal, 'subtotal')
    minimo = float(linha['minimo_subtotal'])
    if sub < minimo:
        raise ApiErro(f'Subtotal mínimo de R$ {minimo:.2f} para este cupom')
    tipo = linha['tipo_desconto']
    if tipo not in TIPOS_DESCONTO:
        raise ApiErro('Tipo de desconto do cupom inválido')
    frete = decimal(frete, 'frete')
    if tipo == 'percentual':
        desconto = sub * float(linha['valor_desconto']) / 100
    elif tipo == 'frete':
        desconto = frete
    else:
        desconto = float(linha['valor_desconto'])
    return {
        'id': linha['id'],
        'codigo': linha['codigo'],
        'desconto': round(min(desconto, sub + frete), 2)
    }


def fechar(dados):
    usuario_id = sessao.exigir_logado()
    usuario = usuario_repo.obter_por_id(usuario_id)
    if not usuario['cpf']:
        raise ApiErro('Complete seu cadastro com CPF antes de finalizar o pedido')

    itens = _itens_consolidados(dados.get('itens'))
    forma = texto_obrigatorio(dados.get('forma_pagamento'), 'forma_pagamento')
    if forma not in FORMAS:
        raise ApiErro('Forma de pagamento inválida (use cartao, pix ou boleto)')
    endereco = dados.get('endereco') or {}
    if not isinstance(endereco, dict):
        raise ApiErro('Informe o endereço de entrega')
    cep_entrega = _cep_valido(endereco.get('cep'))
    frete = ZONAS_FRETE[cep_entrega[0]]

    produzidos = []
    subtotal = 0.0
    for produto_id, quantidade in itens.items():
        produto = produto_repo.obter(produto_id)
        if produto is None or not produto['ativo']:
            raise ApiErro(f'Produto {produto_id} não encontrado', 400)
        if produto['estoque_qtd'] < quantidade:
            raise ApiErro(f'Estoque insuficiente para "{produto["nome"]}" '
                          f'({produto["estoque_qtd"]} disponíveis)')
        preco = float(produto['preco'])
        subtotal += preco * quantidade
        produzidos.append({'produto_id': produto_id, 'quantidade': quantidade,
                           'preco_unitario': preco})

    cupom = None
    if dados.get('cupom'):
        cupom = validar_cupom(dados.get('cupom'), subtotal, frete)

    desconto = cupom['desconto'] if cupom else 0.0
    subtotal = round(subtotal, 2)
    total = round(max(subtotal + frete - desconto, 0), 2)

    with db.transacao() as cur:
        endereco_linha = endereco_repo.inserir({
            'usuario_id': usuario_id,
            'cep': cep_entrega,
            'logradouro': texto_obrigatorio(endereco.get('logradouro'), 'endereco.logradouro'),
            'numero': texto_obrigatorio(endereco.get('numero'), 'endereco.numero'),
            'complemento': texto_opcional(endereco.get('complemento')),
            'bairro': texto_obrigatorio(endereco.get('bairro'), 'endereco.bairro'),
            'cidade': texto_obrigatorio(endereco.get('cidade'), 'endereco.cidade'),
            'estado': _estado_valido(endereco.get('estado'))
        }, cur=cur)
        pedido_linha = pedido_repo.inserir({
            'usuario_id': usuario_id,
            'cupom_id': cupom['id'] if cupom else None,
            'subtotal': subtotal,
            'frete': frete,
            'desconto': desconto,
            'total': total,
            'status': 'pendente',
            'forma_pagamento': forma,
            'cep_entrega': cep_entrega
        }, cur=cur)
        for prod in produzidos:
            pedido_repo.inserir_item(pedido_linha['id'], prod['produto_id'],
                                     prod['quantidade'], prod['preco_unitario'],
                                     cur=cur)
    pedido = detalhar(pedido_linha['id'])
    pedido['endereco_id'] = endereco_linha['id']
    return pedido


def _itens_consolidados(itens):
    if not isinstance(itens, list) or not itens:
        raise ApiErro('Informe os itens do pedido')
    consolidados = {}
    for item in itens:
        if not isinstance(item, dict):
            raise ApiErro('Formato de item inválido')
        produto_id = inteiro(item.get('id'), 'itens.id')
        quantidade = inteiro(item.get('q', item.get('quantidade')), 'itens.q')
        if quantidade <= 0:
            raise ApiErro('Quantidade deve ser maior que zero')
        consolidados[produto_id] = consolidados.get(produto_id, 0) + quantidade
    return consolidados


def listar():
    usuario = usuario_repo.obter_por_id(sessao.exigir_logado())
    linhas = pedido_repo.listar() if usuario['admin'] \
        else pedido_repo.listar(usuario['id'])
    return [_formatar(l) for l in linhas]


def detalhar(pedido_id):
    pedido_id = inteiro(pedido_id, 'pedido_id')
    linha = pedido_repo.obter(pedido_id)
    if linha is None:
        raise ApiErro('Pedido não encontrado', 404)
    sessao.exigir_dono(linha['usuario_id'])
    pedido = _formatar(linha)
    pedido['itens'] = [{'id': i['id'], 'produto_id': i['produto_id'],
                        'nome': i['nome'], 'quantidade': i['quantidade'],
                        'preco_unitario': float(i['preco_unitario'])}
                       for i in pedido_repo.itens_de(pedido_id)]
    return pedido


def cancelar(pedido_id):
    linha = pedido_repo.obter(inteiro(pedido_id, 'pedido_id'))
    if linha is None:
        raise ApiErro('Pedido não encontrado', 404)
    sessao.exigir_dono(linha['usuario_id'])
    if linha['status'] not in ('pendente', 'pago'):
        raise ApiErro('Pedidos enviados ou entregues não podem ser cancelados')
    pedido_repo.atualizar_status(linha['id'], 'cancelado')
    return {'mensagem': 'Pedido cancelado', 'status': 'cancelado'}


def atualizar_status(pedido_id, status):
    sessao.exigir_admin()
    linha = pedido_repo.obter(inteiro(pedido_id, 'pedido_id'))
    if linha is None:
        raise ApiErro('Pedido não encontrado', 404)
    status = texto_obrigatorio(status, 'status')
    if status not in STATUSES:
        raise ApiErro('Status inválido (use pendente, pago, enviado, '
                      'entregue ou cancelado)')
    linha = pedido_repo.atualizar_status(linha['id'], status)
    return {'mensagem': 'Status atualizado', 'status': linha['status']}


def _formatar(linha):
    return {
        'id': linha['id'],
        'usuario_id': linha['usuario_id'],
        'usuario_nome': linha.get('usuario_nome'),
        'cupom_id': linha['cupom_id'],
        'subtotal': float(linha['subtotal']),
        'frete': float(linha['frete']),
        'desconto': float(linha['desconto']),
        'total': float(linha['total']),
        'status': linha['status'],
        'forma_pagamento': linha['forma_pagamento'],
        'cep_entrega': linha['cep_entrega'],
        'criado_em': str(linha['criado_em'])
    }


def _cep_valido(valor):
    cep = validators.normalizar_cep(valor)
    if cep is None:
        raise ApiErro('CEP inválido (informe os 8 dígitos)')
    return cep


def _estado_valido(valor):
    if not validators.valida_estado(valor):
        raise ApiErro('Estado deve ser a sigla com 2 letras (ex.: SP)')
    return str(valor).strip().upper()


