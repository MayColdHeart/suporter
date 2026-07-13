import pymysql
import pymysql.cursors
from flask import g, current_app


def get_db():
    """Retorna (e cria se necessário) a conexão da requisição atual."""
    if "db" not in g:
        cfg = current_app.config
        g.db = pymysql.connect(
            host=cfg["MARIADB_HOST"],
            port=cfg["MARIADB_PORT"],
            user=cfg["MARIADB_USER"],
            password=cfg["MARIADB_PASSWORD"],
            database=cfg["MARIADB_DB"],
            charset=cfg["MARIADB_CHARSET"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
    return g.db


def get_cursor():
    return get_db().cursor()


def commit():
    """Realiza commit na conexão da requisição atual."""
    get_db().commit()


def close_db(error=None):
    """Fecha a conexão ao término da requisição (registrado via teardown)."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Registra o teardown de conexão na aplicação Flask."""
    app.teardown_appcontext(close_db)