# core/routes/sales.py
from flask import Blueprint, render_template
from flask_login import login_required

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/')
@login_required
def sales():
    return render_template('sales.html', title='المبيعات')
