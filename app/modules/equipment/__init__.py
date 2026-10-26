from flask import Blueprint

equipment_bp = Blueprint('equipment', __name__)

from app.modules.equipment import routes  # noqa: E402, F401
