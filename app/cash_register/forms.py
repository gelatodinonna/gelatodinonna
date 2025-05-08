# app/cash_register/forms.py
from flask_wtf import FlaskForm
from wtforms import DecimalField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CashRegisterForm(FlaskForm):
    amount         = DecimalField('Ποσό', validators=[DataRequired()])
    date           = DateField('Ημερομηνία', format='%Y-%m-%d', validators=[DataRequired()])
    payment_source = SelectField('Πηγή Χρημάτων', choices=[('cash','Μετρητά'),('card','Κάρτα'),('delivery','Delivery')],validators=[DataRequired()])
    store_id       = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    submit         = SubmitField('Καταχώρηση')

class CashForm(FlaskForm):
    """Μόνο CSRF token, δεν χρειάζεται πεδία."""
    pass    