from flask import Blueprint, render_template
from app.models import Revenue, Expense
from app.extensions import db
from sqlalchemy import func

# Ορισμός του blueprint για τα οικονομικά
financial_bp = Blueprint('financial', __name__, url_prefix='/financials')

# Route για την προβολή της χρηματοοικονομικής κατάστασης
@financial_bp.route('/')
def financial_home():
    # Υπολογισμός του συνολικού ποσού εσόδων
    total_revenue = db.session.query(func.sum(Revenue.amount)).scalar() or 0
    # Υπολογισμός του συνολικού ποσού εξόδων
    total_expense = db.session.query(func.sum(Expense.amount)).scalar() or 0
    # Υπολογισμός του καθαρού ισοζυγίου
    net_balance = total_revenue - total_expense

    # Επιστροφή στο template των οικονομικών
    return render_template('financial/index.html', total_revenue=total_revenue, total_expense=total_expense, net_balance=net_balance)