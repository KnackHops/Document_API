from os import path
import sys

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from flaskr import create_app

app, socketio = create_app()

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # _app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
    socketio.run(app, debug=True)