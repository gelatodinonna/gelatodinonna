from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import Store

class PeriodForm(FlaskForm):
    start_date = DateField(
        'Ημ/νία Έναρξης',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )
    end_date = DateField(
        'Ημ/νία Λήξης',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )
    store_id = SelectField(
        'Κατάστημα',
        coerce=int,
        choices=[(0, 'Όλα τα Καταστήματα')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Δημιουργία Αναφοράς')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Φορτώνουμε τα καταστήματα από τη βάση
        stores = Store.query.order_by(Store.name).all()
        self.store_id.choices = [(0, 'Όλα τα Καταστήματα')] + [(s.id, s.name) for s in stores]