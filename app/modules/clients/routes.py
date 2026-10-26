from flask import render_template
from flask_login import login_required
from app.modules.clients import clients_bp
from app.models.client import Client

@clients_bp.route('/')
@login_required
def list_clients():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template('clients/list.html', clients=clients)
