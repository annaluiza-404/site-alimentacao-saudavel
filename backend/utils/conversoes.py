from utils.erros import ApiErro


def inteiro(valor, campo):
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ApiErro(f'{campo.replace("_", " ")} deve ser um número inteiro')


def decimal(valor, campo, casas=None):
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise ApiErro(f'{campo.replace("_", " ")} deve ser um número')
    return round(numero, casas) if casas is not None else numero


def texto_obrigatorio(valor, campo):
    texto = (str(valor or '')).strip()
    if not texto:
        raise ApiErro(f'{campo.replace("_", " ")} é obrigatório')
    return texto


def texto_opcional(valor):
    return (str(valor or '')).strip() or None
