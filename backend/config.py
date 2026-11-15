import os


def ler_dotenv(caminho):
    if not os.path.exists(caminho):
        return
    with open(caminho, encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith('#') or '=' not in linha:
                continue
            chave, valor = linha.split('=', 1)
            os.environ.setdefault(chave.strip(), valor.strip())


def carregar(app):
    ler_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    app.config['DB'] = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', '5432')),
        'nome': os.environ.get('DB_NAME', 'alimentacao_saudavel'),
        'user': os.environ.get('DB_USER', 'iz_app'),
        'senha': os.environ.get('DB_PASS', 'iz_dev_password')
    }
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'iz-dev-secret-key')
