from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
from app.models import Store

class FlavorForm(FlaskForm):
    name = StringField('Όνομα Γεύσης', validators=[DataRequired()])
    stores = SelectMultipleField(
        'Καταστήματα με διαθέσιμη τη γεύση',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # φορτώνουμε επιλογές καταστημάτων
        choices = [(s.id, s.name) for s in Store.query.order_by(Store.name)]
        self.stores.choices = choices