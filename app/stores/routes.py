from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions    import db
from app.models        import Store, Expense, Revenue    # <-- Εδώ τα Expense & Revenue
from app.stores.forms  import StoreForm

stores_bp = Blueprint('stores', __name__, url_prefix='/stores')

@stores_bp.route('/')
def store_list():
    stores = Store.query.order_by(Store.name).all()
    return render_template('stores/index.html', stores=stores)

@stores_bp.route('/new', methods=['GET','POST'])
def new_store():
    form = StoreForm()
    if form.validate_on_submit():
        s = Store(
            name         = form.name.data,
            location     = form.location.data,
            company      = form.company.data or None,
            ownership_pct= form.ownership_pct.data
        )
        db.session.add(s); db.session.commit()
        flash('Κατάστημα προστέθηκε', 'success')
        return redirect(url_for('stores.store_list'))
    return render_template('stores/new.html', form=form)

@stores_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_store(id):
    s = Store.query.get_or_404(id)
    form = StoreForm(obj=s)
    if form.validate_on_submit():
        s.name          = form.name.data
        s.location      = form.location.data
        s.company       = form.company.data or None
        s.ownership_pct = form.ownership_pct.data
        db.session.commit()
        flash('Τα στοιχεία ενημερώθηκαν', 'success')
        return redirect(url_for('stores.store_list'))
    return render_template('stores/edit.html', form=form, store=s)

@stores_bp.route('/delete/<int:id>', methods=['GET','POST'])
def delete_store(id):
    s = Store.query.get_or_404(id)
    if request.method=='POST':
        # εδώ δεν σβήνουμε τα revenue/expense, απλά τα κρατάμε χωρίς κατάστημα
        from app.models import Expense, Revenue
        Expense.query.filter_by(store_id=id).update({'store_id': None})
        Revenue.query.filter_by(store_id=id).update({'store_id': None})
        db.session.delete(s)
        db.session.commit()
        flash('Κατάστημα διαγράφηκε.', 'warning')
        return redirect(url_for('stores.store_list'))
    return render_template('stores/delete.html', store=s)