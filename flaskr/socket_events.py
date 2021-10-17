from flaskr import _socketio

from flask import Blueprint

bp = Blueprint("socket_events", __name__)


@_socketio.on('connect')
def handle_connection():
    print('AYE!')


@_socketio.on('message')
def handle_mesage(strin):
    print(strin)


@_socketio.event
def hello(strin):
    print(strin)