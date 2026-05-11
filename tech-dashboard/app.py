
import os
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash, jsonify
)
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

app.config["MYSQL_HOST"]     = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"]     = os.getenv("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"]       = os.getenv("MYSQL_DB", "tech_dashboard")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# helpers

def get_cursor():
    return mysql.connection.cursor()


def supervisor_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "supervisor":
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated


def tecnico_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "tecnico":
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated

#todas as rotas

@app.route("/")
def index():
    if session.get("role") == "supervisor":
        return redirect(url_for("supervisor_dashboard"))
    if session.get("role") == "tecnico":
        return redirect(url_for("tecnico_status"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role  = request.form.get("role")   # "supervisor" ou "tecnico"
        id_   = request.form.get("id")
        senha = request.form.get("senha")

        cur = get_cursor()

        if role == "supervisor":
            cur.execute(
                "SELECT * FROM supervisores WHERE id = %s AND senha = %s",
                (id_, senha)
            )
            user = cur.fetchone()
            if user:
                session["role"]    = "supervisor"
                session["user_id"] = user["id"]
                session["name"]    = user["name"]
                return redirect(url_for("supervisor_dashboard"))

        elif role == "tecnico":
            cur.execute(
                "SELECT * FROM tecnicos WHERE id = %s AND senha = %s",
                (id_, senha)
            )
            user = cur.fetchone()
            if user:
                session["role"]    = "tecnico"
                session["user_id"] = user["id"]
                session["name"]    = user["name"]
                return redirect(url_for("tecnico_status"))

        flash("ID ou senha inválidos.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


#rota — supervisor


@app.route("/supervisor")
@supervisor_required
def supervisor_dashboard():
    cur = get_cursor()
    cur.execute("SELECT * FROM tecnicos ORDER BY name")
    tecnicos = cur.fetchall()
    return render_template("supervisor/dashboard.html", tecnicos=tecnicos)


@app.route("/supervisor/tecnico/adicionar", methods=["POST"])
@supervisor_required
def supervisor_adicionar_tecnico():
    name  = request.form.get("name", "").strip()
    senha = request.form.get("senha", "").strip()

    if not name or not senha:
        flash("Nome e senha são obrigatórios.", "error")
        return redirect(url_for("supervisor_dashboard"))

    cur = get_cursor()
    cur.execute(
        "INSERT INTO tecnicos (name, senha) VALUES (%s, %s)",
        (name, senha)
    )
    mysql.connection.commit()
    flash(f'Técnico "{name}" adicionado com sucesso.', "success")
    return redirect(url_for("supervisor_dashboard"))


@app.route("/supervisor/tecnico/<int:tecnico_id>/editar", methods=["POST"])
@supervisor_required
def supervisor_editar_tecnico(tecnico_id):
    name  = request.form.get("name", "").strip()
    senha = request.form.get("senha", "").strip()

    cur = get_cursor()
    if senha:
        cur.execute(
            "UPDATE tecnicos SET name = %s, senha = %s WHERE id = %s",
            (name, senha, tecnico_id)
        )
    else:
        cur.execute(
            "UPDATE tecnicos SET name = %s WHERE id = %s",
            (name, tecnico_id)
        )
    mysql.connection.commit()
    flash("Técnico atualizado.", "success")
    return redirect(url_for("supervisor_dashboard"))


@app.route("/supervisor/tecnico/<int:tecnico_id>/deletar", methods=["POST"])
@supervisor_required
def supervisor_deletar_tecnico(tecnico_id):
    cur = get_cursor()
    cur.execute("DELETE FROM tecnicos WHERE id = %s", (tecnico_id,))
    mysql.connection.commit()
    flash("Técnico removido.", "success")
    return redirect(url_for("supervisor_dashboard"))


# rota - tecnico

@app.route("/tecnico")
@tecnico_required
def tecnico_status():
    cur = get_cursor()
    cur.execute(
        "SELECT * FROM tecnicos WHERE id = %s",
        (session["user_id"],)
    )
    tecnico = cur.fetchone()
    return render_template("tecnico/status.html", tecnico=tecnico)


@app.route("/tecnico/status", methods=["POST"])
@tecnico_required
def tecnico_atualizar_status():
    novo_status   = request.form.get("status")
    qtd_chamados  = request.form.get("qtd_chamados")

    cur = get_cursor()

    if novo_status in ("disponivel", "em_atendimento"):
        cur.execute(
            "UPDATE tecnicos SET status = %s WHERE id = %s",
            (novo_status, session["user_id"])
        )

    if qtd_chamados is not None:
        cur.execute(
            "UPDATE tecnicos SET qtd_chamados = %s WHERE id = %s",
            (int(qtd_chamados), session["user_id"])
        )

    mysql.connection.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"ok": True})

    return redirect(url_for("tecnico_status"))


# dados em tempo real

@app.route("/api/tecnicos")
@supervisor_required
def api_tecnicos():
    cur = get_cursor()
    cur.execute("SELECT id, name, status, qtd_chamados FROM tecnicos ORDER BY name")
    return jsonify(cur.fetchall())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)