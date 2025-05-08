from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Personnel, Store
from app.personnel.forms import PersonnelForm
from app.extensions import db

personnel_bp = Blueprint('personnel', __name__, url_prefix='/personnel')

@personnel_bp.route('/')
@login_required
def personnel_home():
    staff = Personnel.query.order_by(Personnel.last_name).all()
    return render_template('personnel/index.html', staff=staff)

@personnel_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_personnel():
    form = PersonnelForm()
    if form.validate_on_submit():
        p = Personnel(
            username    = form.username.data,
            first_name  = form.first_name.data,
            last_name   = form.last_name.data,
            father_name = form.father_name.data,
            age         = form.age.data,
            vat         = form.vat.data,
            amka        = form.amka.data,
            telephone   = form.telephone.data,
            address     = form.address.data,
            iban        = form.iban.data,
            ama         = form.ama.data,
        )
        p.set_password(form.password.data)
        selected = form.stores.data
        p.stores = Store.query.filter(Store.id.in_(selected)).all()

        db.session.add(p)
        db.session.commit()
        flash('Το μέλος προσωπικού προστέθηκε!', 'success')
        return redirect(url_for('personnel.personnel_home'))

    return render_template('personnel/new.html', form=form)

@personnel_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_personnel(id):
    p = Personnel.query.get_or_404(id)
    form = PersonnelForm(obj=p)
    form.stores.data = [s.id for s in p.stores]

    if form.validate_on_submit():
        p.username    = form.username.data
        if form.password.data:
            p.set_password(form.password.data)
        p.first_name  = form.first_name.data
        p.last_name   = form.last_name.data
        p.father_name = form.father_name.data
        p.age         = form.age.data
        p.vat         = form.vat.data
        p.amka        = form.amka.data
        p.telephone   = form.telephone.data
        p.address     = form.address.data
        p.iban        = form.iban.data
        p.ama         = form.ama.data
        selected = form.stores.data
        p.stores = Store.query.filter(Store.id.in_(selected)).all()

        db.session.commit()
        flash('Η καταχώριση ενημερώθηκε!', 'success')
        return redirect(url_for('personnel.personnel_home'))

    return render_template('personnel/edit.html', form=form, person=p)

@personnel_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_personnel(id):
    p = Personnel.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Διαγράφηκε το μέλος προσωπικού.', 'warning')
    return redirect(url_for('personnel.personnel_home'))