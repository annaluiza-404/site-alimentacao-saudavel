from repositories.base_repo import executar


def inserir(dados, cur=None):
    return executar(
        'INSERT INTO enderecos (usuario_id, cep, logradouro, numero, complemento, '
        'bairro, cidade, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
        (dados['usuario_id'], dados['cep'], dados['logradouro'], dados['numero'],
         dados.get('complemento'), dados['bairro'], dados['cidade'], dados['estado']),
        one=True, cur=cur)
