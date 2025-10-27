from . import bp2

@bp2.route("/")
async def index():
    return "Hello From Second Blueprint"

