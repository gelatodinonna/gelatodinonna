from flask_wtf import FlaskForm
from wtforms import DecimalField, DateField, SelectField, StringField
from wtforms.validators import InputRequired

class ExpenseForm(FlaskForm):
    amount = DecimalField('Amount', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
    supplier_vat = StringField('Supplier VAT')
    store_id = SelectField('Store', coerce=int, validators=[InputRequired()])