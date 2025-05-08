from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

from app.models import Store

class MaterialForm(FlaskForm):
    code     = StringField('Κωδικός',   validators=[DataRequired(), Length(max=50)])
    name     = StringField('Όνομα',     validators=[DataRequired(), Length(max=100)])
    quantity = FloatField('Ποσότητα',  validators=[DataRequired()])
    unit     = StringField('Μονάδα',    validators=[DataRequired(), Length(max=20)])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    submit   = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Γεμίζουμε το dropdown με τα διαθέσιμα καταστήματα
        stores = Store.query.order_by(Store.name).all()
        self.store_id.choices = [(s.id, s.name) for s in stores]