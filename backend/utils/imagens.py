import os
import uuid

PASTA_UPLOADS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
EXTENSOES = {'jpg', 'jpeg', 'png', 'webp'}
TAMANHO_MAX = 2 * 1024 * 1024


class ErroImagem(Exception):
    pass


def salvar_imagem(arquivo, subpasta='produtos'):
    if arquivo is None or not arquivo.filename:
        return None
    nome = arquivo.filename
    if '.' not in nome:
        raise ErroImagem('Arquivo de imagem sem extensao')
    extensao = nome.rsplit('.', 1)[-1].lower()
    if extensao not in EXTENSOES:
        raise ErroImagem(f"Extensao '{extensao}' nao permitida (use jpg, png ou webp)")
    arquivo.seek(0, os.SEEK_END)
    tamanho = arquivo.tell()
    arquivo.seek(0)
    if tamanho > TAMANHO_MAX:
        raise ErroImagem('Imagem maior que 2MB')
    if tamanho == 0:
        raise ErroImagem('Arquivo de imagem vazio')
    pasta = os.path.join(PASTA_UPLOADS, subpasta)
    os.makedirs(pasta, exist_ok=True)
    nome_salvo = f'{uuid.uuid4().hex}.{extensao}'
    arquivo.save(os.path.join(pasta, nome_salvo))
    return f'uploads/{subpasta}/{nome_salvo}'
