# app/cash_register/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Revenue
from .forms import CashRegisterForm

cash_register_bp = Blueprint('cash_register', __name__, url_prefix='/cash-register')

@cash_register_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_cash():
    form = CashRegisterForm()
    # Παίρνουμε μόνο τα καταστήματα που ανήκουν στον χρήστη
    stores = current_user.stores
    if not stores:
        flash(
            "Δεν έχετε επιλεγμένα καταστήματα. "
            "Παρακαλώ επικοινωνήστε με τον διαχειριστή.",
            'danger'
        )
        return redirect(url_for('dashboard.dashboard'))
    form.store_id.choices = [(s.id, s.name) for s in stores]

    if form.validate_on_submit():
        revenue = Revenue(
            amount=form.amount.data,
            date=form.date.data,
            category="Καθημερινό Ταμείο",
            store_id=form.store_id.data
        )
        db.session.add(revenue)
        db.session.commit()

        flash('Το ταμείο καταχωρήθηκε επιτυχώς!', 'success')
        return redirect(url_for('cash_register.view_cash'))

    return render_template('cash_register/add_cash.html', form=form)

@cash_register_bp.route('/view')
@login_required
def view_cash():
    # Φιλτράρουμε τα έσοδα για όλα τα καταστήματα του χρήστη
    store_ids = [s.id for s in current_user.stores]
    registers = Revenue.query.filter(Revenue.store_id.in_(store_ids)).all()
    
    form = CashRegisterForm()   
    return render_template('cash_register/view_cash.html',registers=registers,form=form) 

@cash_register_bp.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_cash(id):
    revenue = Revenue.query.get_or_404(id)
    form = CashRegisterForm(obj=revenue)

    # Ξαναγεμίζουμε το dropdown με τα καταστήματα του χρήστη
    stores = current_user.stores
    form.store_id.choices = [(s.id, s.name) for s in stores]

    if form.validate_on_submit():
        revenue.amount   = form.amount.data
        revenue.date     = form.date.data
        revenue.store_id = form.store_id.data
        db.session.commit()
        flash('Το ταμείο ενημερώθηκε επιτυχώς!', 'success')
        return redirect(url_for('cash_register.view_cash'))

    return render_template('cash_register/add_cash.html', form=form)

@cash_register_bp.route('/delete/<int:id>', methods=['POST','GET'])
@login_required
def delete_cash(id):
    revenue = Revenue.query.get_or_404(id)
    db.session.delete(revenue)
    db.session.commit()
    flash('Το ταμείο διαγράφηκε.', 'warning')
    return redirect(url_for('cash_register.view_cash'))