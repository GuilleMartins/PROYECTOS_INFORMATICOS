from flask import render_template
from flask_login import login_required
from app.modules.workshop import workshop_bp
from app.models.inventory import Part

@workshop_bp.route('/')
@login_required
def index():
    parts = Part.query.order_by(Part.name.asc()).all()
    return render_template('workshop/index.html', parts=parts)
