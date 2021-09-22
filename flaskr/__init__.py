import os
from flask import Flask

_app = None

def create_app():
    _app = app = Flask(__name__, instance_relative_config=True)

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return '<h1>Hi! You are accessing my root! <a href="">Here is the link for the api!</a><h1>'

    return app

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     _app.run(host='0.0.0.0', port=port)