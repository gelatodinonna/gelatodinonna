from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from app.models import Store

class PersonnelForm(FlaskForm):
    username    = StringField('Username',
                     validators=[DataRequired(), Length(min=4, max=64)])
    password    = PasswordField('Password',
                     validators=[DataRequired(), Length(min=6)])
    confirm     = PasswordField('Confirm Password',
                     validators=[DataRequired(), EqualTo('password', message='Οι κωδικοί δεν ταιριάζουν')])
    first_name  = StringField('Όνομα',     validators=[Optional(), Length(max=50)])
    last_name   = StringField('Επίθετο',   validators=[Optional(), Length(max=50)])
    father_name = StringField('Πατρώνυμο', validators=[Optional(), Length(max=50)])
    age         = IntegerField('Ηλικία',   validators=[Optional()])
    vat         = StringField('ΑΦΜ',        validators=[Optional(), Length(max=20)])
    amka        = StringField('ΑΜΚΑ',       validators=[Optional(), Length(max=11)])
    telephone   = StringField('Τηλέφωνο',   validators=[Optional(), Length(max=20)])
    address     = StringField('Διεύθυνση',  validators=[Optional(), Length(max=200)])
    iban        = StringField('IBAN',       validators=[Optional(), Length(max=34)])
    ama         = StringField('ΑΜΑ',        validators=[Optional(), Length(max=20)])
    stores      = SelectMultipleField('Καταστήματα', coerce=int, validators=[Optional()])
    submit      = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stores = Store.query.order_by(Store.name).all()
        self.stores.choices = [(s.id, s.name) for s in stores]