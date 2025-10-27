from . import bp1

@bp1.route("/")
async def index():
    return "Hello From First Blueprint"

