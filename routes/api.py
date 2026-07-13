from flask import Blueprint, jsonify
from database import get_cursor
from decorators import supervisor_required

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/tecnicos")
@supervisor_required
def tecnicos():
    """Retorna lista atualizada de técnicos para o polling do dashboard."""
    cur = get_cursor()
    cur.execute(
        "SELECT id, name, status, qtd_chamados FROM tecnicos ORDER BY name"
    )
    return jsonify(cur.fetchall())