import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'μυστικό_για_ανάπτυξη')
    # if you set DATABASE_URL envvar, use it (e.g. on Render/Heroku/…);
    # otherwise we fall back to a local SQLite in instance/app.db
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or 'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False