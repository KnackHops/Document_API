from flaskr import _celery
from flask import Blueprint

bp = Blueprint("tasks", __name__)


@_celery.task()
def send_mail():
    pass
