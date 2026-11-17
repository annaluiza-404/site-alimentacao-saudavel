import json
import urllib.error
import urllib.request

from flask import current_app

from utils.conversoes import texto_obrigatorio
from utils.erros import ApiErro
from repositories import produto_repo, receita_repo, categoria_repo, cupom_repo

URL_OPENAI = 'https://api.openai.com/v1/chat/completions'
LIMITE_PERGUNTA = 500
LIMITE_HISTORICO = 6
TEMPERATURA = 0.6
MAX_TOKENS = 300


def responder(pergunta, historico=None):
    pergunta = texto_obrigatorio(pergunta, 'pergunta')
    if len(pergunta) > LIMITE_PERGUNTA:
        raise ApiErro(f'Pergunta deve ter no máximo {LIMITE_PERGUNTA} caracteres')
    config = current_app.config.get('OPENAI', {})
    chave = config.get('chave')
    if not chave:
        raise ApiErro('Chatbot indisponível: configure OPENAI_API_KEY no backend/.env', 503)

    mensagens = [{'role': 'system', 'content': _prompt_sistema()}]
    mensagens.extend(_historico(historico))
    mensagens.append({'role': 'user', 'content': pergunta})

    corpo = {
        'model': config.get('modelo') or 'gpt-4o-mini',
        'messages': mensagens,
        'temperature': TEMPERATURA,
        'max_tokens': MAX_TOKENS
    }
    requisicao = urllib.request.Request(
        URL_OPENAI,
        data=json.dumps(corpo).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {chave}'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(requisicao, timeout=25) as resposta:
            dados = json.loads(resposta.read())
    except urllib.error.HTTPError as erro:
        detalhe = ''
        try:
            detalhe = json.loads(erro.read()).get('error', {}).get('message', '')
        except Exception:
            detalhe = ''
        mensagem = f'Falha ao consultar o chatbot ({erro.code})'
        raise ApiErro(mensagem + (f': {detalhe}' if detalhe else ''), 502)
    except (urllib.error.URLError, TimeoutError, ValueError):
        raise ApiErro('Chatbot temporariamente indisponível', 503)

    try:
        return dados['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError, TypeError):
        raise ApiErro('Resposta inválida do chatbot', 502)


def _historico(historico):
    mensagens = []
    for item in (historico or [])[-LIMITE_HISTORICO:]:
        if not isinstance(item, dict):
            continue
        papel = item.get('papel')
        conteudo = (item.get('conteudo') or '').strip()
        if papel in ('user', 'bot') and conteudo:
            mensagens.append({
                'role': 'user' if papel == 'user' else 'assistant',
                'content': conteudo[:1000]
            })
    return mensagens


def _brl(valor):
    return 'R$ ' + f'{float(valor):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def _prompt_sistema():
    produtos = [f"- {p['nome_produto']} ({_brl(p['preco'])}, "
                f"{p['estoque_qtd']} em estoque, marca {p['nome_marca']})"
                for p in produto_repo.listar({})]
    receitas = [f"- {r['titulo']} (categoria {r['categoria']})"
                for r in receita_repo.listar()]
    categorias = categoria_repo.listar()
    cats_produto = ', '.join(c['nome'] for c in categorias if c['tipo'] == 'produto')
    cats_restr = ', '.join(c['nome'] for c in categorias if c['tipo'] == 'restricao')
    cupons = []
    for c in cupom_repo.listar_ativos():
        if c['tipo_desconto'] == 'percentual':
            desc = f"{float(c['valor_desconto']):.0f}% de desconto"
        elif c['tipo_desconto'] == 'frete':
            desc = 'zera o frete'
        else:
            desc = f"{_brl(c['valor_desconto'])} de desconto"
        minimo = float(c['minimo_subtotal'])
        if minimo > 0:
            desc += f" (subtotal mínimo {_brl(minimo)})"
        cupons.append(f"- {c['codigo']}: {desc}")
    return (
        'Você é o ChuchuBot, assistente virtual da Intolerância Zero, uma loja de '
        'alimentação saudável sem glúten e sem lactose. Responda em português do Brasil, '
        'de forma curta, simpática e objetiva (no máximo 4 frases). Responda somente '
        'sobre o site, produtos, preços, entregas, cupons, receitas e alimentação com '
        'restrições. Não faça diagnósticos nem prescreva tratamentos: quando for o caso, '
        'oriente procurar médico ou nutricionista. Nunca invente produtos que não estejam '
        'na lista abaixo.\n\n'
        'Produtos disponíveis no catálogo:\n' + ('\n'.join(produtos) or '- nenhum') +
        '\n\nCategorias de produto: ' + (cats_produto or 'nenhuma') +
        '\nRestrições alimentares: ' + (cats_restr or 'nenhuma') +
        '\n\nConteúdos e receitas do site:\n' + ('\n'.join(receitas) or '- nenhum') +
        '\n\nCupons ativos:\n' + ('\n'.join(cupons) or '- nenhum') +
        '\n\nFrete por região do CEP; formas de pagamento: pix, cartão e boleto.'
    )
