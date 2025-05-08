from flask_login import login_required
from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from app.models import Expense, Store
from app.expenses.forms import ExpenseForm
from app.extensions import db

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/')
@login_required
def expense_home():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('expenses/index.html', expenses=expenses)

@expenses_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            amount=form.amount.data,
            date=form.date.data,
            supplier_vat=form.supplier_vat.data,
            store_id=form.store_id.data,
            payment_source=form.payment_source.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Το έξοδο καταχωρήθηκε επιτυχώς!', 'success')
        return redirect(url_for('expenses.expense_home'))
    return render_template('expenses/new.html', form=form)

@expenses_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.date = form.date.data
        expense.supplier_vat = form.supplier_vat.data
        expense.store_id = form.store_id.data
        expense.payment_source = form.payment_source.data
        db.session.commit()
        flash('Η καταχώριση ενημερώθηκε επιτυχώς!', 'success')
        return redirect(url_for('expenses.expense_home'))
    return render_template('expenses/edit.html', form=form, expense=expense)

@expenses_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)

    # Dummy form μόνο για CSRF protection
    class DummyForm(FlaskForm):
        pass

    form = DummyForm()

    if form.validate_on_submit():    # θα περάσει μόνο στο POST με έγκυρο CSRF token
        db.session.delete(expense)
        db.session.commit()
        flash('Η καταχώριση διαγράφηκε επιτυχώς!', 'success')
        return redirect(url_for('expenses.expense_home'))

    # Στο GET στέλνουμε το form ώστε το template να μπορεί να καλέσει form.hidden_tag()
    return render_template('expenses/delete.html', expense=expense, form=form)