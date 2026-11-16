import db


def executar(sql, params=(), one=False, cur=None):
    if cur is None:
        return db.query(sql, params, one=one)
    cur.execute(sql, params)
    linhas = cur.fetchall() if cur.description else []
    if one:
        return linhas[0] if linhas else None
    return linhas
