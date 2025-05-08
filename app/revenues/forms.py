from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import Store

class RevenueForm(FlaskForm):
    date = DateField(
        'Ημερομηνία Εσόδου',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )
    store_id = SelectField(
        'Κατάστημα',
        coerce=int,
        choices=[],
        validators=[DataRequired()]
    )
    category = SelectField(
        'Κατηγορία',
        choices=[
            ('wholesale', 'Χονδρική'),
            ('retail',    'Λιανική'),
        ],
        validators=[DataRequired()]
    )
    amount = FloatField(
        'Ποσό (€)',
        validators=[DataRequired()]
    )
    submit = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super(RevenueForm, self).__init__(*args, **kwargs)
        # Γεμίζουμε το dropdown από τα καταστήματα
        self.store_id.choices = [
            (s.id, s.name) for s in Store.query.order_by(Store.name).all()
        ]