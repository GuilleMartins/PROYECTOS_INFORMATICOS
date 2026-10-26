from datetime import datetime
from app.extensions import db

class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='RESTRICT'), nullable=False)
    equipment_type = db.Column(db.String(50), nullable=False) # Notebook, PC, Celular, etc.
    brand = db.Column(db.String(60), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    serial_number = db.Column(db.String(100))
    physical_condition = db.Column(db.Text) # Rayones, golpes, tornillos faltantes
    accessories = db.Column(db.Text)        # Cargador, mochila, cable
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    client = db.relationship('Client', back_populates='equipments')
    orders = db.relationship('Order', back_populates='equipment', lazy='dynamic')

    @property
    def display_name(self):
        sn = f" (S/N: {self.serial_number})" if self.serial_number else ""
        return f"{self.equipment_type} {self.brand} {self.model}{sn}"

    def __repr__(self):
        return f'<Equipment {self.id} - {self.display_name}>'
