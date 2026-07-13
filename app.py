"""
app.py
------
Application factory do Flask.
Importa configurações, inicializa o banco e registra os blueprints.
"""

from flask import Flask
from config import Config
import database


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa o módulo de banco de dados (registra teardown)
    database.init_app(app)

    # Registra blueprints
    from routes.auth       import bp as auth_bp
    from routes.supervisor import bp as supervisor_bp
    from routes.tecnico    import bp as tecnico_bp
    from routes.api        import bp as api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(supervisor_bp)
    app.register_blueprint(tecnico_bp)
    app.register_blueprint(api_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])