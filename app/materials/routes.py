# app/materials/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models import Material
from .forms import MaterialForm

materials_bp = Blueprint('materials', __name__, url_prefix='/materials')

@materials_bp.route('/', methods=['GET'])
@login_required
def index():
    # Εμφανίζουμε όλα τα υλικά (ή φίλτραρε με .filter_by(store_id=...) αν θες)
    materials = Material.query.all()
    return render_template('materials/index.html', materials=materials)

@materials_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = MaterialForm()
    if form.validate_on_submit():
        m = Material(
            code     = form.code.data,
            name     = form.name.data,
            quantity = form.quantity.data,
            unit     = form.unit.data,
            store_id = form.store_id.data
        )
        db.session.add(m)
        db.session.commit()
        flash('Το υλικό προστέθηκε στην αποθήκη!', 'success')
        return redirect(url_for('materials.index'))

    return render_template('materials/new.html', form=form)

@materials_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    m = Material.query.get_or_404(id)
    form = MaterialForm(obj=m)
    if form.validate_on_submit():
        m.code     = form.code.data
        m.name     = form.name.data
        m.quantity = form.quantity.data
        m.unit     = form.unit.data
        m.store_id = form.store_id.data
        db.session.commit()
        flash('Υλικό ενημερώθηκε!', 'success')
        return redirect(url_for('materials.index'))

    return render_template('materials/edit.html', form=form, material=m)

@materials_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    m = Material.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(m)
        db.session.commit()
        flash('Υλικό διαγράφηκε!', 'success')
        return redirect(url_for('materials.index'))

    return render_template('materials/delete.html', material=m)