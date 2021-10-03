from flask import (
    Blueprint, request, make_response
)

from . import temp_db

bp = Blueprint("document", __name__, url_prefix="/document")

docu_lists = temp_db.docu_lists
user_pinned = temp_db.user_pinned
login_data = temp_db.login_data


@bp.route("/fetch/")
def fetch():
    id = int(request.args.get('id'))
    which_get = request.args.get('which_get')
    global docu_lists
    global user_pinned

    if len(docu_lists) == 0:
        return make_response(({'_documents': None}, 200))
    else:
        if len(user_pinned) == 0:
            if which_get == 'pinned':
                return make_response(({'_documents': None}, 200))
            if which_get == 'nonpinned':
                return make_response(({'_documents': docu_lists}, 200))
            if which_get == 'default':
                return_doc = []

                for doc in docu_lists:
                    return_doc.append({
                        **doc,
                        'pinned': False
                    })

                print(return_doc, docu_lists)

                return make_response(({'_documents': return_doc}, 200))

        new_doc = []

        for doc in docu_lists:
            for each_pin in user_pinned:
                if each_pin['docid'] == doc['id']:
                    if each_pin['userid'] == id:
                        new_doc.append({
                            **doc,
                            'pinned': True
                        })
            if len(new_doc) == 0:
                new_doc.append({
                    **doc,
                    'pinned': False
                })
            else:
                if not doc['id'] == new_doc[-1]['id']:
                    new_doc.append({
                        **doc,
                        'pinned': False
                    })

        if which_get == 'default':
            return make_response(({'_documents': new_doc}, 200))
        
        return_doc = []

        for doc in new_doc:
            if doc['pinned'] and which_get == 'pinned':
                return_doc.append(doc)

            if not doc['pinned'] and which_get == 'nonpinned':
                return_doc.append(doc)

        if len(return_doc) == 0:
            return make_response(({'_documents': None}, 200))

        return make_response(({'_documents': return_doc}, 200))


@bp.route("/add", methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        global docu_lists
        
        if len(docu_lists) == 0:
            id = 0
            docu_lists.append({'id': id,
                               'title': request.json['title'],
                               'document': request.json['document']})
        else:
            id = docu_lists[-1]['id'] + 1
            docu_lists.append({'id': id,
                               'title': request.json['title'],
                               'document': request.json['document']})
        return {'id': id}, 200


@bp.route("/edit", methods=('GET', 'PUT'))
def edit():
    if request.method == 'PUT':
        id = request.json['id']
        title = request.json['title']
        document = request.json['document']
        global docu_lists

        if len(docu_lists) == 0:
            return {'error': 'No document to update'}, 500
        else:
            new_docu = []
            for docu in docu_lists:
                per_docu = docu
                if docu['id'] == id:
                    if not docu['title'] == title:
                        return {'error', 'Title not found'}, 409
                    else:
                        per_docu['document'] = document

                new_docu.append(per_docu)

            docu_lists = new_docu

            return "", 204


@bp.route('/pin-doc', methods=('GET', 'POST'))
def pin_doc():
    if request.method == 'POST':
        global user_pinned
        global login_data

        userid = request.json['userid']
        docid = request.json['docid']
        doctitle = request.json['doctitle']

        found = False
        exist = False
        for user_login in login_data:
            if user_login['id'] == userid:
                for doc in docu_lists:
                    if doc['id'] == docid:
                        found = True
                        for each_pinned in user_pinned:
                            if each_pinned['userid'] == userid:
                                if each_pinned['docid'] == docid:
                                    exist = True

                        if not exist:
                            user_pinned.append({
                                'userid': userid,
                                'docid': docid,
                                'doctitle': doctitle
                            })
                        else:
                            return {'error': 'already pinned!'}, 409

        if found:
            return '', 204
        else:
            return {'error': 'error pinning'}, 409


@bp.route('/unpin-doc/', methods=('GET', 'DELETE'))
def unpin_doc():
    if request.method == 'DELETE':
        global login_data
        global docu_lists
        global user_pinned
        userid = int(request.args.get('userid'))
        docid = int(request.args.get('docid'))

        found = False
        for user_login in login_data:
            if user_login['id'] == userid:
                for doc in docu_lists:
                    if doc['id'] == docid:
                        found = True

        if found:
            new_pinned = []
            for each_pinned in user_pinned:
                if not each_pinned['userid'] == userid and not each_pinned['docid'] == docid:
                    new_pinned.append(each_pinned)

            user_pinned = new_pinned
            return '', 204
        else:
            return {'error': 'error unpin'}, 409