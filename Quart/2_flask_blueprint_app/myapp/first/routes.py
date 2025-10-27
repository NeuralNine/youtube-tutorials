from . import bp1

@bp1.route("/")
def index():
    return "Hello From First Blueprint"

