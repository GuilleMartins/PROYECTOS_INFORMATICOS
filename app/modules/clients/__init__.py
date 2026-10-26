from flask import Blueprint

clients_bp = Blueprint('clients', __name__)

from app.modules.clients import routes  # noqa: E402, F401
