from flask import Blueprint

portal_bp = Blueprint('portal', __name__, url_prefix='/consulta')

from app.modules.portal import routes  # noqa: E402, F401
