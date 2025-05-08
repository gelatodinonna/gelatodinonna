# app/production/forms.py

from flask_wtf import FlaskForm
from wtforms import DateTimeField, SelectField, FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import Store, Flavor

class ProductionForm(FlaskForm):
    date = DateTimeField(
        'Ημ/νία & Ώρα',
        format='%Y-%m-%dT%H:%M',   # Ταιριάζει με το input type="datetime-local"
        validators=[DataRequired()]
    )
    store_id = SelectField(
        'Κατάστημα',
        coerce=int,
        validators=[DataRequired()]
    )
    flavor_id = SelectField(
        'Γεύση',
        coerce=int,
        validators=[DataRequired()]
    )
    quantity = FloatField(
        'Ποσότητα',
        validators=[DataRequired()]
    )
    unit = SelectField(
        'Μονάδα Μέτρησης',
        choices=[('kg', 'Κιλά'), ('l', 'Λίτρα'), ('pcs', 'Τεμάχια')],
        validators=[DataRequired()]
    )
    batch_code = StringField(
        'Batch Code',
        validators=[DataRequired(), Length(max=32)],
        render_kw={'readonly': True}
    )
    submit = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Φορτώνουμε τα καταστήματα για το dropdown
        stores = Store.query.order_by(Store.name).all()
        self.store_id.choices = [(s.id, s.name) for s in stores]
        # Φορτώνουμε τις γεύσεις
        flavors = Flavor.query.order_by(Flavor.name).all()
        self.flavor_id.choices = [(f.id, f.name) for f in flavors]