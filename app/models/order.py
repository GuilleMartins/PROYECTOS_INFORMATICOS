from datetime import datetime
import uuid
from app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False, index=True) # Ej: OT-2026-0001
    public_token = db.Column(db.String(36), unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4()))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='RESTRICT'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id', ondelete='RESTRICT'), nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    assigned_tech_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    reported_failure = db.Column(db.Text, nullable=False)
    current_status = db.Column(db.String(40), nullable=False, default='RECIBIDO', index=True)
    priority = db.Column(db.String(20), nullable=False, default='NORMAL') # BAJA, NORMAL, ALTA, URGENTE
    
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    estimated_delivery_date = db.Column(db.Date, nullable=True)
    completion_date = db.Column(db.DateTime, nullable=True)
    delivery_date = db.Column(db.DateTime, nullable=True)
    qr_code_path = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    client = db.relationship('Client', back_populates='orders')
    equipment = db.relationship('Equipment', back_populates='orders')
    creator = db.relationship('User', foreign_keys=[created_by_user_id], back_populates='orders_created')
    technician = db.relationship('User', foreign_keys=[assigned_tech_id], back_populates='orders_assigned')

    # Componentes de taller y auditoría
    history = db.relationship('OrderStatusHistory', back_populates='order', cascade='all, delete-orphan', order_by='OrderStatusHistory.created_at.desc()')
    diagnostic = db.relationship('Diagnostic', back_populates='order', uselist=False, cascade='all, delete-orphan')
    budget = db.relationship('Budget', back_populates='order', uselist=False, cascade='all, delete-orphan')
    quality_control = db.relationship('QualityControl', back_populates='order', uselist=False, cascade='all, delete-orphan')
    delivery = db.relationship('Delivery', back_populates='order', uselist=False, cascade='all, delete-orphan')

    @property
    def status_badge_class(self):
        badges = {
            'RECIBIDO': 'secondary',
            'EN_DIAGNOSTICO': 'info',
            'PENDIENTE_APROBACION': 'warning text-dark',
            'PRESUPUESTO_APROBADO': 'primary',
            'EN_REPARACION': 'primary',
            'EN_CONTROL_CALIDAD': 'info',
            'LISTO_ENTREGA': 'success',
            'ENTREGADO': 'dark',
            'CANCELADO': 'danger'
        }
        return badges.get(self.current_status, 'light')

    @property
    def status_label(self):
        labels = {
            'RECIBIDO': 'Recibido en Taller',
            'EN_DIAGNOSTICO': 'En Diagnóstico',
            'PENDIENTE_APROBACION': 'Pendiente de Aprobación',
            'PRESUPUESTO_APROBADO': 'Presupuesto Aprobado',
            'EN_REPARACION': 'En Reparación',
            'EN_CONTROL_CALIDAD': 'En Control de Calidad',
            'LISTO_ENTREGA': 'Listo para Entrega',
            'ENTREGADO': 'Entregado al Cliente',
            'CANCELADO': 'Cancelado'
        }
        return labels.get(self.current_status, self.current_status)

    def __repr__(self):
        return f'<Order {self.order_number} ({self.current_status})>'


class OrderStatusHistory(db.Model):
    __tablename__ = 'order_status_history'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    previous_status = db.Column(db.String(40), nullable=True)
    new_status = db.Column(db.String(40), nullable=False)
    changed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    changed_by_role = db.Column(db.String(40), nullable=False) # 'ADMIN', 'TECNICO', 'CLIENTE_QR'
    observation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    order = db.relationship('Order', back_populates='history')
    user = db.relationship('User')

    def __repr__(self):
        return f'<History {self.order_id}: {self.previous_status} -> {self.new_status}>'
