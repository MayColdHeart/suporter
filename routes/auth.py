from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash,
)
from database import get_cursor

bp = Blueprint("auth", __name__)


@bp.route("/")
def index():
    """Redireciona conforme o perfil logado."""
    if session.get("role") == "supervisor":
        return redirect(url_for("supervisor.dashboard"))
    if session.get("role") == "tecnico":
        return redirect(url_for("tecnico.status"))
    return redirect(url_for("auth.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role  = request.form.get("role")   # "supervisor" ou "tecnico"
        id_   = request.form.get("id")
        senha = request.form.get("senha")

        cur = get_cursor()

        if role == "supervisor":
            cur.execute(
                "SELECT * FROM supervisores WHERE id = %s AND senha = %s",
                (id_, senha),
            )
            user = cur.fetchone()
            if user:
                session["role"]    = "supervisor"
                session["user_id"] = user["id"]
                session["name"]    = user["name"]
                return redirect(url_for("supervisor.dashboard"))

        elif role == "tecnico":
            cur.execute(
                "SELECT * FROM tecnicos WHERE id = %s AND senha = %s",
                (id_, senha),
            )
            user = cur.fetchone()
            if user:
                session["role"]    = "tecnico"
                session["user_id"] = user["id"]
                session["name"]    = user["name"]
                return redirect(url_for("tecnico.status"))

        flash("ID ou senha inválidos.", "error")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))