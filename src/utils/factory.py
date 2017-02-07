from flask import Flask
from flask_cors import CORS


def create_app(package_name, config, blueprints=None, extensions=None):
    app = Flask(package_name)
    app.config.from_object(config)
    config.init_app(app)
    CORS(app)
    if blueprints:
        for bp in blueprints:
            app.register_blueprint(bp)
    if extensions:
        for extension in extensions:

            extension.init_app(app)

    return app
