from flask import render_template
from flask_login import login_required
from app.modules.orders import orders_bp
from app.models.order import Order

@orders_bp.route('/')
@login_required
def list_orders():
    orders = Order.query.order_by(Order.entry_date.desc()).all()
    return render_template('orders/list.html', orders=orders)
