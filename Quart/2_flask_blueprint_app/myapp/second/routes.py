from . import bp2

@bp2.route("/")
def index():
    return "Hello From Second Blueprint"

