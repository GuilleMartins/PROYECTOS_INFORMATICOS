from flask import render_template
from flask_login import login_required, current_user
from app.modules.dashboard import dashboard_bp
from app.models.order import Order
from app.models.client import Client
from app.models.inventory import Part

@dashboard_bp.route('/')
@login_required
def index():
    # Métricas generales para el dashboard (Fase 5)
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(current_status='RECIBIDO').count()
    diagnostic_orders = Order.query.filter_by(current_status='EN_DIAGNOSTICO').count()
    approval_orders = Order.query.filter_by(current_status='PENDIENTE_APROBACION').count()
    repairing_orders = Order.query.filter_by(current_status='EN_REPARACION').count()
    ready_orders = Order.query.filter_by(current_status='LISTO_ENTREGA').count()
    delivered_orders = Order.query.filter_by(current_status='ENTREGADO').count()
    
    recent_orders = Order.query.order_by(Order.entry_date.desc()).limit(5).all()
    total_clients = Client.query.count()
    low_stock_parts = Part.query.filter(Part.stock_quantity <= Part.min_stock_alert).count()

    return render_template(
        'dashboard/index.html',
        total_orders=total_orders,
        pending_orders=pending_orders,
        diagnostic_orders=diagnostic_orders,
        approval_orders=approval_orders,
        repairing_orders=repairing_orders,
        ready_orders=ready_orders,
        delivered_orders=delivered_orders,
        recent_orders=recent_orders,
        total_clients=total_clients,
        low_stock_parts=low_stock_parts
    )
