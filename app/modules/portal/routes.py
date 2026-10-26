from flask import Blueprint

portal_bp = Blueprint('portal', __name__, url_prefix='/consulta')

@portal_bp.route('/<token>')
def view_order(token):
    return f"Consulta pública para orden con token {token}"
