from flask import Blueprint

revenues_bp = Blueprint('revenues', __name__, template_folder='templates')

from . import routes