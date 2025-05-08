from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, ChangePasswordForm
from app.extensions import db
from app.models import Personnel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Personnel.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Καλωσήρθες, {}'.format(user.first_name), 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.dashboard'))
        flash('Λανθασμένο username ή κωδικός', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Έγινε επιτυχής αποσύνδεση.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Ο παλιός κωδικός δεν είναι σωστός.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Ο κωδικός άλλαξε επιτυχώς!', 'success')
            return redirect(url_for('dashboard.dashboard'))
    return render_template('auth/change_password.html', form=form)