from flask_login import login_required
from flask_login import login_required
from flask import render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import Flavor, Store
from .forms import FlavorForm
from . import flavors_bp

@flavors_bp.route('/')
@login_required
def index():
    flavors = Flavor.query.order_by(Flavor.name).all()
    return render_template('flavors/index.html', flavors=flavors)

@flavors_bp.route('/new', methods=['GET','POST'])
@login_required
def new_flavor():
    form = FlavorForm()
    if form.validate_on_submit():
        f = Flavor(name=form.name.data)
        # αποθήκευση σχέσεων
        f.stores = Store.query.filter(Store.id.in_(form.stores.data)).all()
        db.session.add(f)
        db.session.commit()
        flash('Γεύση προστέθηκε!', 'success')
        return redirect(url_for('flavors.index'))
    return render_template('flavors/new.html', form=form)

@flavors_bp.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_flavor(id):
    f = Flavor.query.get_or_404(id)
    form = FlavorForm(obj=f)
    if form.validate_on_submit():
        f.name = form.name.data
        f.stores = Store.query.filter(Store.id.in_(form.stores.data)).all()
        db.session.commit()
        flash('Γεύση ενημερώθηκε!', 'success')
        return redirect(url_for('flavors.index'))
    # προκαθορισμένες επιλογές
    form.stores.data = [s.id for s in f.stores]
    return render_template('flavors/edit.html', form=form, flavor=f)

@flavors_bp.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_flavor(id):
    f = Flavor.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(f)
        db.session.commit()
        flash('Γεύση διαγράφηκε!', 'success')
        return redirect(url_for('flavors.index'))
    return render_template('flavors/delete.html', flavor=f)