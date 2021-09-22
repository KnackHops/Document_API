from flask import (
    Blueprint, request, make_response
)

bp = Blueprint("document", __name__, url_prefix="/document")
docu_lists = []


@bp.route("/add", methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        if len(docu_lists) == 0:
            docu_lists.append({'id': 0,
                               'title': request.json['title'],
                               'document': request.json['document']})
        else:
            docu_lists.append({'id': len(docu_lists),
                               'title': request.json['title'],
                               'document': request.json['document']})
        return '', 204


@bp.route("/fetch")
def fetch():
    if len(docu_lists) == 0:
        return_docu_list = None
    else:
        return_docu_list = docu_lists

    return make_response(({'documents': return_docu_list}, 200))


@bp.after_request
def after_request_func(response):
    response.headers['Content-Type'] = 'application/json'
    return response

