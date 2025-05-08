from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Revenue
from app.revenues.forms import RevenueForm
from app.extensions import db

revenues_bp = Blueprint('revenues', __name__, url_prefix='/revenues')

@revenues_bp.route('/')
def revenue_home():
    revenues = Revenue.query.order_by(Revenue.date.desc()).all()
    return render_template('revenues/index.html', revenues=revenues)

@revenues_bp.route('/new', methods=['GET','POST'])
def new_revenue():
    form = RevenueForm()
    if form.validate_on_submit():
        rev = Revenue(
            date=form.date.data,
            amount=form.amount.data,
            category=form.category.data,
            store_id=form.store_id.data
        )
        db.session.add(rev)
        db.session.commit()
        flash('Το έσοδο καταχωρήθηκε!', 'success')
        return redirect(url_for('revenues.revenue_home'))
    return render_template('revenues/new.html', form=form)

@revenues_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_revenue(id):
    rev = Revenue.query.get_or_404(id)
    form = RevenueForm(obj=rev)
    if form.validate_on_submit():
        rev.date      = form.date.data
        rev.amount    = form.amount.data
        rev.category  = form.category.data
        rev.store_id  = form.store_id.data
        db.session.commit()
        flash('Η καταχώριση ενημερώθηκε!', 'success')
        return redirect(url_for('revenues.revenue_home'))
    return render_template('revenues/edit.html', form=form, revenue=rev)

@revenues_bp.route('/delete/<int:id>', methods=['GET','POST'])
def delete_revenue(id):
    rev = Revenue.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(rev)
        db.session.commit()
        flash('Το έσοδο διαγράφηκε!', 'success')
        return redirect(url_for('revenues.revenue_home'))
    return render_template('revenues/delete.html', revenue=rev)