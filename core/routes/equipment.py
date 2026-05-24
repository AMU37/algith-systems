# core/routes/equipment.py
from flask import Blueprint, render_template
from flask_login import login_required

equipment_bp = Blueprint('equipment', __name__, url_prefix='/equipment')

@equipment_bp.route('/')
@login_required
def equipment():
    return render_template('equipment.html', title='المعدات')

@equipment_bp.route('/fuel')
@login_required
def fuel():
    return render_template('fuel.html', title='المحروقات')