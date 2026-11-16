from repositories.base_repo import executar


def obter_por_codigo(codigo, cur=None):
    return executar('SELECT id, codigo, tipo_desconto, valor_desconto, '
                    'minimo_subtotal, data_validade FROM cupons '
                    'WHERE codigo = %s AND ativo', (codigo,), one=True, cur=cur)
