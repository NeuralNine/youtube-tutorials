from quart import Quart

def create_app():
    app = Quart(__name__)

    from .first import bp1 as first_bp
    from .second import bp2 as second_bp

    app.register_blueprint(first_bp)
    app.register_blueprint(second_bp)

    return app

