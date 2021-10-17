from os import path

import sys

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from flaskr import create_app

app, socketio = create_app()


@app.route('/')
def index():
    return f'<h1>Hi! You are accessing my root! ' \
           f'<a href="https://github.com/KnackHops/Document_API">' \
           f'Here is the link for the api!</a> <h1>'


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # _app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
