"""
routes/tecnico.py
-----------------
Blueprint do técnico: ver e atualizar status/chamados.
"""

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, jsonify,
)
from database import get_cursor, commit
from decorators import tecnico_required

bp = Blueprint("tecnico", __name__, url_prefix="/tecnico")


@bp.route("/")
@tecnico_required
def status():
    cur = get_cursor()
    cur.execute("SELECT * FROM tecnicos WHERE id = %s", (session["user_id"],))
    tecnico = cur.fetchone()
    return render_template("tecnico/status.html", tecnico=tecnico)


@bp.route("/status", methods=["POST"])
@tecnico_required
def atualizar_status():
    novo_status  = request.form.get("status")
    qtd_chamados = request.form.get("qtd_chamados")

    cur = get_cursor()

    if novo_status in ("disponivel", "em_atendimento"):
        cur.execute(
            "UPDATE tecnicos SET status = %s WHERE id = %s",
            (novo_status, session["user_id"]),
        )

    if qtd_chamados is not None:
        cur.execute(
            "UPDATE tecnicos SET qtd_chamados = %s WHERE id = %s",
            (int(qtd_chamados), session["user_id"]),
        )

    commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"ok": True})

    return redirect(url_for("tecnico.status"))