from flask import Blueprint, render_template
from datetime import datetime
from sqlalchemy import func
from app.reports.forms import PeriodForm
from app.models import Revenue, Expense
from app.extensions import db

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/', methods=['GET','POST'])
def period_report():
    form = PeriodForm()
    report = None

    if form.validate_on_submit():
        start    = form.start_date.data
        end      = form.end_date.data
        store_id = form.store_id.data

        # κλείσιμο end στο τέλος της μέρας
        end_dt = datetime(end.year, end.month, end.day, 23, 59, 59)

        # βασικά query για λίστες
        rev_q = Revenue.query.filter(Revenue.date >= start, Revenue.date <= end_dt)
        exp_q = Expense.query.filter(Expense.date >= start, Expense.date <= end_dt)

        # αν επιλέξαμε συγκεκριμένο κατάστημα, προσθέτουμε φίλτρο
        if store_id != 0:
            rev_q = rev_q.filter(Revenue.store_id == store_id)
            exp_q = exp_q.filter(Expense.store_id == store_id)

        revs = rev_q.order_by(Revenue.date).all()
        exps = exp_q.order_by(Expense.date).all()

        # αθροίσματα
        rev_sum_q = db.session.query(func.sum(Revenue.amount)).filter(Revenue.date >= start, Revenue.date <= end_dt)
        exp_sum_q = db.session.query(func.sum(Expense.amount)).filter(Expense.date >= start, Expense.date <= end_dt)
        if store_id != 0:
            rev_sum_q = rev_sum_q.filter(Revenue.store_id == store_id)
            exp_sum_q = exp_sum_q.filter(Expense.store_id == store_id)

        total_rev = rev_sum_q.scalar() or 0
        total_exp = exp_sum_q.scalar() or 0

        report = {
            'start': start, 'end': end,
            'revenues': revs, 'expenses': exps,
            'total_rev': total_rev, 'total_exp': total_exp,
            'net': total_rev - total_exp
        }

    return render_template('reports/period.html', form=form, report=report)