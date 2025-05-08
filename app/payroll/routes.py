from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Payroll
from .forms import PayrollForm

payroll_bp = Blueprint('payroll', __name__, url_prefix='/payroll')

@payroll_bp.route('/', methods=['GET'])
@login_required
def index():
    # φτιάχνουμε λίστα με όλα τα store_ids του χρήστη
    store_ids = [s.id for s in current_user.stores]
    if not store_ids:
        flash('Δεν έχετε ανατεθειμένα καταστήματα.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    records = (Payroll.query
                    .filter(Payroll.store_id.in_(store_ids))
                    .order_by(Payroll.date.desc())
                    .all())
    return render_template('payroll/index.html', payrolls=records)

@payroll_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = PayrollForm()
    if form.validate_on_submit():
        p = Payroll(
            personnel_id   = form.personnel_id.data,
            store_id       = form.store_id.data,
            date           = form.date.data,
            gross_amount   = form.gross_amount.data,
            net_amount     = form.net_amount.data,
            bonus          = form.bonus.data,
            payment_method = form.payment_method.data
        )
        db.session.add(p)
        db.session.commit()
        flash('Η μισθοδοσία καταχωρήθηκε!', 'success')
        return redirect(url_for('payroll.index'))

    return render_template('payroll/new.html', form=form)

@payroll_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    p = Payroll.query.get_or_404(id)
    form = PayrollForm(obj=p)
    if form.validate_on_submit():
        p.personnel_id   = form.personnel_id.data
        p.store_id       = form.store_id.data
        p.date           = form.date.data
        p.gross_amount   = form.gross_amount.data
        p.net_amount     = form.net_amount.data
        p.bonus          = form.bonus.data
        p.payment_method = form.payment_method.data
        db.session.commit()
        flash('Η μισθοδοσία ενημερώθηκε!', 'success')
        return redirect(url_for('payroll.index'))

    return render_template('payroll/edit.html', form=form, payroll=p)

@payroll_bp.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete(id):
    p = Payroll.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(p)
        db.session.commit()
        flash('Η εγγραφή μισθοδοσίας διαγράφηκε!', 'warning')
        return redirect(url_for('payroll.index'))
    return render_template('payroll/delete.html', payroll=p)