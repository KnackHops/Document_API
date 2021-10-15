from flask import (
    Blueprint, request, make_response
)

from flaskr import temp_db
from flaskr import _qrcode
from flaskr import _socketio

bp = Blueprint("document", __name__, url_prefix="/document")

docu_lists = temp_db.docu_lists
user_pinned = temp_db.user_pinned
login_data = temp_db.login_data
docu_coded = temp_db.docu_coded

socketidLists = {}

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


@bp.route("/fetch-qr/")
def fetch_qr():
    docid = int(request.args.get('docid'))
    global docu_coded

    if len(docu_coded) > 0:
        for doc in docu_coded:
            if doc['docid'] == docid:
                return make_response(({'qr_code': doc['qr_code']}, 200))
    else:
        return '', 204


@bp.route('/fetch-doc-qr/')
def fetch_doc_qr():
    str_code = request.args.get('str_code')
    userid = request.args.get('userid')
    global docu_coded
    global docu_lists
    global user_pinned

    if len(docu_coded) > 0:
        for doc in docu_coded:
            if doc['str_code'] == str_code:
                docid = doc['docid']

        _doc = None
        for doc in docu_lists:
            if doc['id'] == docid:
                _doc = {
                    'id': docid,
                    'title': doc['title'],
                    'body': doc['document']
                }

        if not _doc:
            return '', 204

        if len(user_pinned) == 0:
            _doc['pinned'] = False
            return make_response(({'document': _doc}, 200))
        else:
            for each_pin in user_pinned:
                if each_pin['userid'] == userid and each_pin['docid'] == docid:
                    _doc['pinned'] = True

            if 'pinned' not in _doc:
                _doc['pinned'] = False

            return make_response(({'document': _doc}, 200))

        return '', 204
    else:
        return '', 204


def generate_QR(id, title):
    _id = str(id)

    _id_length = len(_id);

    if _id_length < 6:
        ran = 6 - _id_length

        filler = ""
        for c in range(ran):
            filler = filler + "f"
        new_id = filler + _id

    str_code = "doc/" + new_id + "/doc/" + title

    return [_qrcode(str_code), str_code]


@bp.route("/add", methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        global docu_lists
        global docu_coded

        title = request.json['title']
        document = request.json['document']

        if len(docu_lists) == 0:
            id = 0

            qr_code, str_code = generate_QR(id, title)
        else:
            id = docu_lists[-1]['id'] + 1

            qr_code, str_code = generate_QR(id, title)

        docu_lists.append({'id': id,
                           'title': title,
                           'document': document})
        docu_coded.append({
            'docid': id,
            'str_code': str_code,
            'qr_code': qr_code
        })

        return make_response(({'id': id, 'qr_code': qr_code}, 200))


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


@_socketio.event
def set_socketid(data):
    new_str = f'user{data["userid"]}'
    socketidLists[new_str] = request.sid
    print(socketidLists)


@_socketio.event
def send_doc(data):
    id_str = f'user{data["userid"]}'
    _socketio.emit("got_sent", data['docid'], to=socketidLists[id_str])
