import re


def valida_email(email):
    return isinstance(email, str) and bool(re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email))


def valida_senha(senha):
    return isinstance(senha, str) and len(senha) >= 6


def valida_cpf(cpf):
    if not isinstance(cpf, str):
        return False
    d = re.sub(r'\D', '', cpf)
    if len(d) != 11 or d == d[0] * 11:
        return False
    soma = sum(int(x) * w for x, w in zip(d[:9], range(10, 1, -1)))
    dv1 = 0 if soma % 11 < 2 else 11 - soma % 11
    if int(d[9]) != dv1:
        return False
    soma = sum(int(x) * w for x, w in zip(d[:10], range(11, 1, -1)))
    dv2 = 0 if soma % 11 < 2 else 11 - soma % 11
    return int(d[10]) == dv2
