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
        g.db = psycopg2.connect(**kwargs)
    return g.db


def fechar_db(_erro=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query(sql, params=(), one=False):
    db = obter_db()
    with db.cursor() as cur:
        cur.execute(sql, params)
        linhas = cur.fetchall() if cur.description else []
    db.commit()
    if one:
        return linhas[0] if linhas else None
    return linhas
