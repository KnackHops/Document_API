from flask import Flask

from instance.config import DevelopmentConfigLocalHost

from conduit.extensions import qrcode
from conduit.extensions import socketio
from conduit.extensions import cors


def create_app(config=None):
    name = __name__.split(".")[0]
    if config:
        app = Flask(name)
    else:
        app = Flask(name, instance_relative_config=True)
        config = DevelopmentConfigLocalHost()

    app.config.from_object(config)

    _socketio = register_extensions(app)
    # register_blueprints(app)

    return app, _socketio


def register_extensions(app):
    qrcode.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    return socketio


def register_blueprints(app):
    from views import document
    from views import user
    from views import socket_events

    cors.init_app(document.bp, origins="*")
    cors.init_app(user.bp, origins="*")

    app.register_blueprint(document.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(socket_events.bp)
