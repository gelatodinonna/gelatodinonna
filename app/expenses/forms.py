from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, DateField, StringField, SelectField
from wtforms.validators import DataRequired
from app.models import Store

class ExpenseForm(FlaskForm):
    amount = FloatField('Ποσό (€)', validators=[DataRequired()])
    date = DateField('Ημερομηνία Εξόδου', format='%Y-%m-%d', validators=[DataRequired()])
    supplier_vat = StringField('Α.Φ.Μ. Προμηθευτή')
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    
    payment_source = SelectField('Πηγή Πληρωμής', choices=[
        ('Χρηματοκιβώτιο', 'Χρηματοκιβώτιο'),
        ('Ταμείο', 'Ταμείο'),
        ('Τραπεζική Συναλλαγή/Κάρτα', 'Τραπεζική Συναλλαγή/Κάρτα')
    ], validators=[DataRequired()])

    submit = SubmitField('Καταχώριση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Γεμίζουμε το dropdown με τα καταστήματα
        self.store_id.choices = [(s.id, s.name) for s in Store.query.order_by(Store.name).all()]