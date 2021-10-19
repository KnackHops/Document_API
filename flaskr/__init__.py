# import os
#
# from functools import wraps
#
# from flask import Flask
# from flask import request
#
# from flask_cors import CORS
# from flask_qrcode import QRcode
# from flask_socketio import SocketIO
# from flask_sqlalchemy import SQLAlchemy
#
# from flaskr.celery_app import create_celery
#
# from instance.config import DevelopmentConfigLocalHost
#
# _app = None
# _qrcode = None
# _socketio = None
# _celery = None
# _sq = None
#
#
# def create_app():
#     global _celery
#     global _qrcode
#     global _socketio
#     global _sq
#
#     app = Flask(__name__, instance_relative_config=True)
#     _sq = SQLAlchemy(app)
#
#     create_folders(app)
#
#     app.config.from_object(DevelopmentConfigLocalHost())
#     print(app.config['CELERY_BROKER_URL'])
#     CORS(app, resources={
#         r'/document/*': {'origins': '*'},
#         r'/*': {'origins': '*'},
#     })
#     _socketio = SocketIO(app, cors_allowed_origins="*")
#     _celery = create_celery(app)
#     _qrcode = QRcode(app)
#
#     @app.route('/')
#     def index():
#         return f'<h1>Hi! You are accessing my root! ' \
#                f'<a href="https://github.com/KnackHops/Document_API">' \
#                f'Here is the link for the api!</a> <h1>'
#
#     @app.after_request
#     def after_request_func(response):
#         if not request.path == "/" and not request.path == '/link-verify/':
#             response.headers['Content-Type'] = 'application/json'
#
#         return response
#
#     from flaskr import document
#     from flaskr import user
#     from flaskr import socket_events
#
#     for compo in [document, user, socket_events]:
#         app.register_blueprint(compo.bp)
#
#     return app
#
#
# def create_folders(app):
#     try:
#         os.mkdir(app.instance_path)
#     except OSError:
#         pass
#
#     try:
#         os.mkdir('tmp')
#     except OSError:
#         pass
#
#
# def valid_wrapper(func):
#     @wraps(func)
#     def inside(*args, **kwargs):
#         if not request.path == "/":
#
#             if len(request.args) > 0:
#                 data = request.args.to_dict()
#             elif request.json:
#                 data = request.json
#             else:
#                 return {'error': 'no data'}, 400
#
#             check_return = validity_check(data)
#
#             if check_return:
#                 return check_return
#
#         return func(*args, **kwargs)
#     return inside
#
#
# def validity_check(list_req):
#     for key in list_req:
#         val = list_req[key]
#         if not val and not val == 0:
#             return {'error': f'{key} is empty'}, 400
#
#     return None
#
#
# def clean_id_wrapper(func):
#     @wraps(func)
#     def inside(*args, **kwargs):
#         if request.args:
#             data = request.args.to_dict()
#         else:
#             data = request.json
#
#         id_lists = id_check(data)
#
#         if id_lists:
#             return func(*args, **kwargs, **id_lists)
#
#         return {"error": "missing values"}, 400
#
#     return inside
#
#
# def id_check(data):
#     key_list_id = ['userid', 'id', 'docid']
#
#     return_list_id = {}
#
#     for key in data:
#         if key in key_list_id:
#             try:
#                 return_list_id[key] = int(data[key])
#             except ValueError:
#                 return False
#
#     return return_list_id
#
#
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     _app.run(host='0.0.0.0', port=port)
#     _app.run(debug=True)
#     _socketio.run(_app, host='127.0.0.1', debug=True)
