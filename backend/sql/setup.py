import os
import argparse
import psycopg2

DIRETORIO = os.path.dirname(os.path.abspath(__file__))


def ler_dotenv():
    caminho = os.path.join(os.path.dirname(DIRETORIO), '.env')
    if not os.path.exists(caminho):
        return
    with open(caminho, encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith('#') or '=' not in linha:
                continue
            chave, valor = linha.split('=', 1)
            os.environ.setdefault(chave.strip(), valor.strip())


def conexao(banco):
    kwargs = {
        'dbname': banco,
        'user': os.environ.get('DB_USER', 'iz_app'),
        'password': os.environ.get('DB_PASS', 'iz_dev_password'),
        'port': int(os.environ.get('DB_PORT', '5432'))
    }
    host = os.environ.get('DB_HOST', 'localhost')
    if host:
        kwargs['host'] = host
    return psycopg2.connect(**kwargs)


def banco_existe(nome):
    with conexao('postgres') as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (nome,))
            return cur.fetchone() is not None


def aplicar(arquivo):
    caminho = os.path.join(DIRETORIO, arquivo)
    with open(caminho, encoding='utf-8') as f:
        sql = f.read()
    conn = conexao(os.environ.get('DB_NAME', 'alimentacao_saudavel'))
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print(f'{arquivo} aplicado')
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='Sobe o schema Intolerância Zero (ddl + objetos + seed) no banco indicado pelas variaveis de ambiente. Onde o banco roda (docker, cluster local, servidor) e indiferente.',
        epilog=(
            'Variaveis (tambem lidas do backend/.env):\n'
            '  DB_HOST   default localhost   (vazio = socket local)\n'
            '  DB_PORT   default 5432\n'
            '  DB_USER   default iz_app\n'
            '  DB_PASS   default iz_dev_password\n'
            '  DB_NAME   default alimentacao_saudavel'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--reset', action='store_true',
                        help='derruba o banco e recria tudo (ddl + objetos + seed)')
    parser.add_argument('--seed', action='store_true',
                        help='aplica apenas o seed.sql (use em banco recem-criado)')
    args = parser.parse_args()

    ler_dotenv()
    nome = os.environ.get('DB_NAME', 'alimentacao_saudavel')

    if args.reset:
        conn = conexao('postgres')
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS {nome} WITH (FORCE)')
        conn.close()
        print(f'banco {nome} derrubado')

    if args.seed:
        if not banco_existe(nome):
            print(f"ERRO: banco '{nome}' nao existe. Rode sem flags primeiro.")
            raise SystemExit(1)
        aplicar('seed.sql')
        print('seed aplicado')
        return

    novo = not banco_existe(nome)
    if novo:
        conn = conexao('postgres')
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f'CREATE DATABASE {nome}')
        conn.close()
        print(f'banco {nome} criado')

    aplicar('ddl.sql')
    aplicar('objetos.sql')

    if novo or args.reset:
        aplicar('seed.sql')
    else:
        print(f'seed pulado (banco {nome} ja existia). Use --reset para recarregar.')

    print(f'banco {nome} pronto')


if __name__ == '__main__':
    main()
