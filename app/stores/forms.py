from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class StoreForm(FlaskForm):
    name = StringField('Όνομα', validators=[DataRequired()])
    location = StringField('Τοποθεσία', validators=[DataRequired()])
    company = StringField('Εταιρεία (προαιρετικό)')
    ownership_pct = FloatField(
        'Ποσοστό (%)',
        default=100.0,
        validators=[NumberRange(min=0, max=100)]
    )
    submit = SubmitField('Αποθήκευση')