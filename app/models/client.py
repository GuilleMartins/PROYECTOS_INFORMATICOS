from datetime import datetime
from app.extensions import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    document_number = db.Column(db.String(30), unique=True, nullable=False, index=True) # Cédula / RUC
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    equipments = db.relationship('Equipment', back_populates='client', cascade='all, delete-orphan', lazy='dynamic')
    orders = db.relationship('Order', back_populates='client', lazy='dynamic')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<Client {self.document_number} - {self.full_name}>'
