# core/routes/purchases.py
from flask import Blueprint, render_template
from flask_login import login_required

purchases_bp = Blueprint('purchases', __name__, url_prefix='/purchases')

@purchases_bp.route('/')
@login_required
def purchases():
    return render_template('purchases.html', title='المشتريات')