from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models import Production
from . import production_bp
from .forms import ProductionForm
import uuid

@production_bp.route('/')
@login_required
def index():
    prods = Production.query.order_by(Production.date.desc()).all()
    return render_template('production/index.html', productions=prods)

@production_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_production():
    form = ProductionForm()
    if request.method == 'GET':
        # Αυτόματο batch_code
        form.batch_code.data = uuid.uuid4().hex[:32]
    if form.validate_on_submit():
        p = Production(
            date       = form.date.data,
            store_id   = form.store_id.data,
            flavor_id  = form.flavor_id.data,
            quantity   = form.quantity.data,
            unit       = form.unit.data,        # Προσθήκη μονάδας
            batch_code = form.batch_code.data
        )
        db.session.add(p)
        db.session.commit()
        flash('Η παραγωγή καταχωρήθηκε!', 'success')
        return redirect(url_for('production.index'))
    return render_template('production/new.html', form=form)

@production_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_production(id):
    p = Production.query.get_or_404(id)
    form = ProductionForm(obj=p)
    if form.validate_on_submit():
        p.date       = form.date.data
        p.store_id   = form.store_id.data
        p.flavor_id  = form.flavor_id.data
        p.quantity   = form.quantity.data
        p.unit       = form.unit.data        # Ενημέρωση μονάδας
        p.batch_code = form.batch_code.data
        db.session.commit()
        flash('Η παραγωγή ενημερώθηκε!', 'success')
        return redirect(url_for('production.index'))
    return render_template('production/edit.html', form=form, prod=p)

@production_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_production(id):
    p = Production.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(p)
        db.session.commit()
        flash('Η παραγωγή διαγράφηκε!', 'success')
        return redirect(url_for('production.index'))
    return render_template('production/delete.html', prod=p)