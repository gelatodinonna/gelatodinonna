from flask import Blueprint

flavors_bp = Blueprint('flavors', __name__, url_prefix='/flavors')

from . import routes  # φορτώνει το routes.py