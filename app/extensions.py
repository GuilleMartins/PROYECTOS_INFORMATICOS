from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instancias compartidas de extensiones de Flask para evitar importaciones circulares
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicie sesión para acceder a este módulo.'
login_manager.login_message_category = 'warning'
