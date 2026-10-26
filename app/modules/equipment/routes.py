from flask import render_template
from flask_login import login_required
from app.modules.equipment import equipment_bp
from app.models.equipment import Equipment

@equipment_bp.route('/')
@login_required
def list_equipment():
    equipments = Equipment.query.order_by(Equipment.created_at.desc()).all()
    return render_template('equipment/list.html', equipments=equipments)
