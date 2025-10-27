from flask import Blueprint

bp2 = Blueprint("second", __name__, url_prefix="/second")

from . import routes

