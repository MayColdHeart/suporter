"""
routes/supervisor.py
--------------------
Blueprint do supervisor: dashboard e CRUD de técnicos.
"""

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash,
)
from database import get_cursor, commit
from decorators import supervisor_required

bp = Blueprint("supervisor", __name__, url_prefix="/supervisor")


@bp.route("/")
@supervisor_required
def dashboard():
    cur = get_cursor()
    cur.execute("SELECT * FROM tecnicos ORDER BY name")
    tecnicos = cur.fetchall()
    return render_template("supervisor/dashboard.html", tecnicos=tecnicos)


@bp.route("/tecnico/adicionar", methods=["POST"])
@supervisor_required
def adicionar_tecnico():
    name  = request.form.get("name", "").strip()
    senha = request.form.get("senha", "").strip()

    if not name or not senha:
        flash("Nome e senha são obrigatórios.", "error")
        return redirect(url_for("supervisor.dashboard"))

    cur = get_cursor()
    cur.execute(
        "INSERT INTO tecnicos (name, senha) VALUES (%s, %s)",
        (name, senha),
    )
    commit()
    flash(f'Técnico "{name}" adicionado com sucesso.', "success")
    return redirect(url_for("supervisor.dashboard"))


@bp.route("/tecnico/<int:tecnico_id>/editar", methods=["POST"])
@supervisor_required
def editar_tecnico(tecnico_id):
    name  = request.form.get("name", "").strip()
    senha = request.form.get("senha", "").strip()

    cur = get_cursor()
    if senha:
        cur.execute(
            "UPDATE tecnicos SET name = %s, senha = %s WHERE id = %s",
            (name, senha, tecnico_id),
        )
    else:
        cur.execute(
            "UPDATE tecnicos SET name = %s WHERE id = %s",
            (name, tecnico_id),
        )
    commit()
    flash("Técnico atualizado.", "success")
    return redirect(url_for("supervisor.dashboard"))


@bp.route("/tecnico/<int:tecnico_id>/deletar", methods=["POST"])
@supervisor_required
def deletar_tecnico(tecnico_id):
    cur = get_cursor()
    cur.execute("DELETE FROM tecnicos WHERE id = %s", (tecnico_id,))
    commit()
    flash("Técnico removido.", "success")
    return redirect(url_for("supervisor.dashboard"))