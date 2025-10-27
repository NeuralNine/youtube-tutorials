from quart import Blueprint

bp1 = Blueprint("first", __name__, url_prefix="/first")

from . import routes

