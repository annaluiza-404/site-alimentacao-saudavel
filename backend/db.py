import contextlib
import psycopg2
import psycopg2.extras
from flask import g, current_app


def init_app(app):
    app.teardown_appcontext(fechar_db)


def obter_db():
    if 'db' not in g:
        cfg = current_app.config['DB']
        kwargs = {
            'dbname': cfg['nome'],
            'user': cfg['user'],
            'password': cfg['senha'],
            'port': cfg['port'],
            'cursor_factory': psycopg2.extras.RealDictCursor
        }
        if cfg['host']:
            kwargs['host'] = cfg['host']
        conexao = psycopg2.connect(**kwargs)
        conexao.autocommit = False
        g.db = conexao
    return g.db


def fechar_db(_erro=None):
    g.pop('em_transacao', None)
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query(sql, params=(), one=False):
    db = obter_db()
    try:
        with db.cursor() as cur:
            cur.execute(sql, params)
            linhas = cur.fetchall() if cur.description else []
        if not g.get('em_transacao'):
            db.commit()
    except Exception:
        if not g.get('em_transacao'):
            db.rollback()
        raise
    if one:
        return linhas[0] if linhas else None
    return linhas


@contextlib.contextmanager
def transacao():
    """Bloco transacional explícito: COMMIT no sucesso, ROLLBACK em exceção.

    O BEGIN é implícito (autocommit desligado). Enquanto o bloco estiver
    aberto, query() não confirma sozinho, para não quebrar a atomicidade.
    """
    if g.get('em_transacao'):
        raise RuntimeError('Transação aninhada não suportada')
    db = obter_db()
    g.em_transacao = True
    try:
        with db.cursor() as cur:
            yield cur
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        g.em_transacao = False
