import os

from flask import (
    Flask, request
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
    # global _socketio
    global _qrcode
    app = Flask(__name__, instance_relative_config=True)
    socketio = SocketIO(app)
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

    from flaskr import document
    from flaskr import user
    # from document import bp as doc_bp
    # from user import bp as user_bp

    for compo in [document, user]:
        app.register_blueprint(compo.bp)

    @app.after_request
    def after_request_func(response):
        if not request.path == "/":
            response.headers['Content-Type'] = 'application/json'
        return response
    # global _app
    # global _socketio
    # _app = app
    # _socketio = socketio
    return app, socketio


# _app = create_app()

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     # _app.run(host='0.0.0.0', port=port)
#     # _app.run(debug=True)
#     _socketio.run(_app, host='0.0.0.0', port=port)