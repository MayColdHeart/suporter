from functools import wraps
from flask import session, redirect, url_for



def supervisor_required(f):
    """Redireciona para / se o usuário não for supervisor."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "supervisor":
            return redirect(url_for("auth.index"))
        return f(*args, **kwargs)
    return decorated


def tecnico_required(f):
    """Redireciona para / se o usuário não for técnico."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "tecnico":
            return redirect(url_for("auth.index"))
        return f(*args, **kwargs)
    return decorated