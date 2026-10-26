from datetime import datetime
from app.extensions import db

class Part(db.Model):
    __tablename__ = 'parts'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(60))
    cost_price = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    selling_price = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    min_stock_alert = db.Column(db.Integer, nullable=False, default=2)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    movements = db.relationship('InventoryMovement', back_populates='part', lazy='dynamic')
    order_parts = db.relationship('OrderPart', back_populates='part', lazy='dynamic')

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.min_stock_alert

    def __repr__(self):
        return f'<Part {self.code} - {self.name} (Stock: {self.stock_quantity})>'


class InventoryMovement(db.Model):
    __tablename__ = 'inventory_movements'

    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id', ondelete='RESTRICT'), nullable=False)
    movement_type = db.Column(db.String(30), nullable=False) # 'ENTRADA', 'SALIDA_REPARACION', 'AJUSTE'
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='SET NULL'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    part = db.relationship('Part', back_populates='movements')
    user = db.relationship('User')
    order = db.relationship('Order')

    def __repr__(self):
        return f'<Movement {self.movement_type} {self.quantity}x Part:{self.part_id}>'
