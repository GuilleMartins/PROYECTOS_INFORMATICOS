import os
from flask import Flask
from app.config import Config
from app.extensions import db, login_manager

def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    # Asegurar que existan directorios de almacenamiento
    os.makedirs(flask_app.config['QR_FOLDER'], exist_ok=True)
    os.makedirs(flask_app.instance_path, exist_ok=True)

    # Inicializar extensiones
    db.init_app(flask_app)
    login_manager.init_app(flask_app)

    # Importar y registrar modelos para SQLAlchemy
    from app import models  # noqa: F401

    # Registro condicional de Blueprints
    from app.modules.auth.routes import auth_bp
    from app.modules.dashboard.routes import dashboard_bp
    from app.modules.clients.routes import clients_bp
    from app.modules.equipment.routes import equipment_bp
    from app.modules.orders.routes import orders_bp
    from app.modules.workshop.routes import workshop_bp
    from app.modules.portal.routes import portal_bp

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(dashboard_bp)
    flask_app.register_blueprint(clients_bp, url_prefix='/clientes')
    flask_app.register_blueprint(equipment_bp, url_prefix='/equipos')
    flask_app.register_blueprint(orders_bp, url_prefix='/ordenes')
    flask_app.register_blueprint(workshop_bp, url_prefix='/taller')
    flask_app.register_blueprint(portal_bp)

    return flask_app
