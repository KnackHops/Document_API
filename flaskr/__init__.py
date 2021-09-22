import os
from flask import Flask
from flask_cors import CORS

_app = None

def create_app():
    _app = app = Flask(__name__, instance_relative_config=True)
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
        return '<h1>Hi! You are accessing my root! <a href="https://github.com/KnackHops/Document_API">Here is the link for the api!</a><h1>'

    from . import document

    for compo in (document,):
        app.register_blueprint(compo.bp)

    return app


# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     _app.run(host='0.0.0.0', port=port)
