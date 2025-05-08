from flask_login import login_required
# app/dashboard/routes.py
from flask_login import login_required
from flask import Blueprint, render_template
from datetime import date
from sqlalchemy import func
from app.extensions import db
from app.models import Revenue, Expense

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def dashboard():
    # σημερινή ημερομηνία
    today = date.today()
    # πρώτη μέρα του τρέχοντος μήνα
    month_start = today.replace(day=1)

    # Έσοδα / Έξοδα ημέρας
    day_rev = db.session.query(func.sum(Revenue.amount))\
                .filter(Revenue.date == today).scalar() or 0
    day_exp = db.session.query(func.sum(Expense.amount))\
                .filter(Expense.date == today).scalar() or 0

    # Έσοδα / Έξοδα μήνα (από 1η μέχρι σήμερα)
    month_rev = db.session.query(func.sum(Revenue.amount))\
                  .filter(Revenue.date >= month_start, Revenue.date <= today)\
                  .scalar() or 0
    month_exp = db.session.query(func.sum(Expense.amount))\
                  .filter(Expense.date >= month_start, Expense.date <= today)\
                  .scalar() or 0

    return render_template('dashboard.html',
                           day_rev=day_rev,
                           day_exp=day_exp,
                           month_rev=month_rev,
                           month_exp=month_exp)