from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(message="Παρακαλώ εισάγετε το username")]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Παρακαλώ εισάγετε τον κωδικό")]
    )
    submit = SubmitField('Σύνδεση')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        'Παλιός Κωδικός',
        validators=[DataRequired(message="Παρακαλώ εισάγετε τον παλιό κωδικό")]
    )
    new_password = PasswordField(
        'Νέος Κωδικός',
        validators=[DataRequired(), Length(min=6, message="Ο κωδικός πρέπει να έχει τουλάχιστον 6 χαρακτήρες")]
    )
    confirm = PasswordField(
        'Επιβεβαίωση Νέου Κωδικού',
        validators=[DataRequired(), EqualTo('new_password', message="Οι κωδικοί δεν ταιριάζουν")]
    )
    submit = SubmitField('Αλλαγή Κωδικού')