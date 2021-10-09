import os
from flask import (
    Flask, send_file
)
from flask_cors import CORS
from flask_qrcode import QRcode
from flask_socketio import (
    SocketIO, emit
)

_app = None
_qrcode = None
_socketio = None


def create_app():
    global _app
    global _qrcode
    global _socketio

    _app = app = Flask(__name__, instance_relative_config=True)
    _socketio = SocketIO(_app)
    _qrcode = QRcode(app)

    CORS(app, resources={
        r'/document/*': {'origins': '*'},
        r'/*': {'origins': '*'}
    })

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():

        return f'<h1>Hi! You are accessing my root! <a href="https://github.com/KnackHops/Document_API">Here is the link for the api!</a> <h1>'

    from . import document
    from . import user

    for compo in [document, user]:
        app.register_blueprint(compo.bp)

    @app.after_request
    def after_request_func(response):
        response.headers['Content-Type'] = 'application/json'
        return response

    return app


if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # _app.run(host='0.0.0.0', port=port)
    _socketio.run(_app, debug=True)
