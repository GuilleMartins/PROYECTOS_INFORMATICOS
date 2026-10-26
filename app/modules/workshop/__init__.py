from flask import Blueprint

workshop_bp = Blueprint('workshop', __name__)

from app.modules.workshop import routes  # noqa: E402, F401
