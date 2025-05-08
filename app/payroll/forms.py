from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_login import current_user
from app.models import Store

class PayrollForm(FlaskForm):
    store_id       = SelectField('Κατάστημα',   coerce=int, validators=[DataRequired()])
    personnel_id   = SelectField('Μέλος Προσωπικού', coerce=int, validators=[DataRequired()])
    date           = DateTimeField('Ημ/νία',   format='%Y-%m-%d', validators=[DataRequired()])
    gross_amount   = FloatField('Μικτό Ποσό',   validators=[DataRequired()])
    net_amount     = FloatField('Καθαρό Ποσό',  validators=[DataRequired()])
    bonus          = FloatField('Μπόνους',      validators=[Optional()])
    payment_method = SelectField(
        'Τρόπος Πληρωμής',
        choices=[('Μετρητά','Μετρητά'),('Τραπεζικό','Τραπεζικό')],
        validators=[DataRequired()]
    )
    submit         = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Παίρνουμε μόνο τα καταστήματα του current_user
        store_choices = [(s.id, s.name) for s in current_user.stores]
        self.store_id.choices = store_choices

        # Personnel: όλο το προσωπικό, ή φιλτράρεις αν θες ανά κατάστημα
        from app.models import Personnel
        staff = Personnel.query.order_by(Personnel.last_name).all()
        self.personnel_id.choices = [
            (p.id, f"{p.first_name or ''} {p.last_name or ''}".strip())
            for p in staff
        ]