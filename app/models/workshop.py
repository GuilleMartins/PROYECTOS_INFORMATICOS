from datetime import datetime
from app.extensions import db

class Diagnostic(db.Model):
    __tablename__ = 'diagnostics'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), unique=True, nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    findings = db.Column(db.Text, nullable=False)
    proposed_solution = db.Column(db.Text, nullable=False)
    technical_notes = db.Column(db.Text)
    diagnostic_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    order = db.relationship('Order', back_populates='diagnostic')
    technician = db.relationship('User')
    budget = db.relationship('Budget', back_populates='diagnostic', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Diagnostic Order:{self.order_id} Tech:{self.technician_id}>'


class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), unique=True, nullable=False)
    diagnostic_id = db.Column(db.Integer, db.ForeignKey('diagnostics.id', ondelete='CASCADE'), nullable=True)
    
    total_parts = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    total_labor = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    
    status = db.Column(db.String(30), nullable=False, default='PENDIENTE') # PENDIENTE, APROBADO, RECHAZADO
    client_notes = db.Column(db.Text)
    decision_date = db.Column(db.DateTime, nullable=True)
    decision_channel = db.Column(db.String(50)) # 'PORTAL_QR', 'PRESENCIAL', 'TELEFONICO'
    decision_ip = db.Column(db.String(45))      # Auditoría de IP
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    order = db.relationship('Order', back_populates='budget')
    diagnostic = db.relationship('Diagnostic', back_populates='budget')
    parts = db.relationship('OrderPart', back_populates='budget', cascade='all, delete-orphan')
    labor_items = db.relationship('OrderLabor', back_populates='budget', cascade='all, delete-orphan')

    def recalculate_totals(self):
        self.total_parts = sum(item.subtotal for item in self.parts)
        self.total_labor = sum(item.price for item in self.labor_items)
        self.total_amount = self.total_parts + self.total_labor

    def __repr__(self):
        return f'<Budget Order:{self.order_id} Total:{self.total_amount} ({self.status})>'


class OrderPart(db.Model):
    __tablename__ = 'order_parts'

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id', ondelete='CASCADE'), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id', ondelete='RESTRICT'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)
    is_consumed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    budget = db.relationship('Budget', back_populates='parts')
    part = db.relationship('Part', back_populates='order_parts')

    def __repr__(self):
        return f'<OrderPart Part:{self.part_id} Qty:{self.quantity}>'


class OrderLabor(db.Model):
    __tablename__ = 'order_labor'

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    estimated_hours = db.Column(db.Numeric(5, 2))
    price = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    budget = db.relationship('Budget', back_populates='labor_items')

    def __repr__(self):
        return f'<OrderLabor {self.description}: {self.price}>'


class QualityControl(db.Model):
    __tablename__ = 'quality_controls'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), unique=True, nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    tests_performed = db.Column(db.Text, nullable=False) # Pruebas funcionales realizadas
    is_approved = db.Column(db.Boolean, nullable=False)   # True = Pasa, False = Rechazado
    observations = db.Column(db.Text)
    check_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    order = db.relationship('Order', back_populates='quality_control')
    technician = db.relationship('User')

    def __repr__(self):
        return f'<QualityControl Order:{self.order_id} Passed:{self.is_approved}>'


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), unique=True, nullable=False)
    delivered_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    receiver_name = db.Column(db.String(120), nullable=False)
    receiver_document = db.Column(db.String(30), nullable=False)
    delivery_notes = db.Column(db.Text)
    delivered_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    order = db.relationship('Order', back_populates='delivery')
    delivered_by = db.relationship('User')

    def __repr__(self):
        return f'<Delivery Order:{self.order_id} Receiver:{self.receiver_name}>'
