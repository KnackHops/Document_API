from flask import (
    Blueprint, request, make_response
)

from . import temp_db

bp = Blueprint("user", __name__)
user_data = temp_db.user_data
login_data = temp_db.login_data
user_pinned = temp_db.user_pinned
user_subordinate = temp_db.user_subordinate


@bp.route('/admin-fetch/')
def admin_fetch():
    # error = None
    # error_code = None
    global login_data
    global user_data

    if len(login_data) > 1:
        users = []
        for user in user_data:
            if not user['id'] == 0 and not user['id'] == int(request.args.get('id')):
                for user_login in login_data:
                    if user_login['id'] == user['id']:

                        users.append({
                            'id': user['id'],
                            'fullname': user['fullname'],
                            'username': user_login['username'],
                            'role': user['role'],
                            'activated': user['activated']
                        })
    else:
        users = None

    return make_response(({'fetched_users': users}, 200))


@bp.route('/subordinate-fetch/')
def friend_fetch():
    global login_data
    global user_data
    global user_subordinate
    id = int(request.args.get('id'))

    if len(login_data) > 1:
        users = []
        for user_login in login_data:
            if not user_login['id'] == id:
                for user_sub in user_subordinate:
                    if user_sub['id'] == id:
                        if user_sub['subordinate_id'] == user_login['id']:
                            for user in user_data:
                                if user['id'] == user_login['id'] and user['activated']:
                                    users.append({
                                        'id': user_login['id'],
                                        'fullname': user['fullname'],
                                        'username': user_login['username'],
                                        'isSubordinate': True,
                                        'mobile': user['mobile'],
                                        'email': user['email']
                                    })

        for user_login in login_data:
            if not user_login['id'] == id:
                is_stranger = True
                activated = None

                for _user in users:
                    if _user['id'] == user_login['id']:
                        is_stranger = False
                if is_stranger:
                    for user in user_data:
                        if user['id'] == user_login['id'] and user['activated']:
                            users.append({
                                'id': user_login['id'],
                                'fullname': user['fullname'],
                                'username': user_login['username'],
                                'isSubordinate': False
                            })

    if len(users) == 0:
        users = None

    return make_response(({'fetched_users': users}, 200))


@bp.route('/send-user-fetch', methods=('GET', 'POST'))
def send_user_fetch():
    if request.method == 'POST':
        docid = request.json['docid']
        id_lists = request.json['id_lists']
        global user_data
        global user_pinned
        print(docid, id_lists)

        if len(user_pinned) == 0:
            return make_response(({'id_filtered': id_lists}, 200))
        else:
            for each_pin in user_pinned:
                for id_user in id_lists:
                    if each_pin['userid'] == id_user['id'] and docid == each_pin['docid']:
                        id_user['pinned'] = True
            return_user = []
            for id_user in id_lists:
                if 'pinned' not in id_user:
                    return_user.append(id_user)

            return make_response(({'id_filtered': return_user}, 200))


@bp.route('/admin-check', methods=('GET', 'POST'))
def admin_check():
    if request.method == 'POST':
        error = 'Server Error'
        error_code = 500
        id = request.json['id']
        password = request.json['password']

        global user_data
        global login_data

        for user in user_data:
            if user['id'] == id:
                if not user['role'] == 'admin':
                    error_code = 409
                    error = "Not an admin!"

        if not error_code == 409:
            for user_login in login_data:
                if user_login['id'] == id:
                    if user_login['password'] == password:
                        return '', 204

        return {'error': error}, error_code


@bp.route('/admin-activate', methods=('GET', 'PUT'))
def admin_activate():
    if request.method == 'PUT':
        error = None
        error_code = None
        id = request.json['id']
        userid = request.json['userid']
        global user_data

        for user in user_data:
            if id == user['id']:
                if not user['role'] == 'admin':
                    error_code = 409
                    error = 'User trying to activate another User is not an admin'

        if error_code:
            return {'error': error}, error_code
        else:
            new_user_data = []
            for user in user_data:
                if userid == user['id']:
                    user['activated'] = not user['activated']
                new_user_data.append(user)

            user_data = new_user_data
            print(user_data)
            return '', 204;


@bp.route('/admin-role-change', methods=('GET', 'PUT'))
def admin_role_change():
    if request.method == 'PUT':
        error = None
        error_code = None
        id = request.json['id']
        userid = request.json['userid']
        role = request.json['role']
        global user_data

        for user in user_data:
            if id == user['id']:
                if not user['role'] == 'admin':
                    error_code = 409
                    error = 'User trying to activate another User is not an admin'

        if error_code:
            return {'error': error}, error_code
        else:
            new_user_data = []
            for user in user_data:
                if userid == user['id']:
                    user['role'] = role
                new_user_data.append(user)

            user_data = new_user_data

            return '', 204;


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # error = None
        # error_code = None
        id = None
        global login_data
        global user_data

        for user_login in login_data:
            if user_login['username'] == request.json['username']:
                if user_login['password'] == request.json['password']:
                    id = user_login['id']

        if id or id == 0:
            return_user = {}
            for user in user_data:
                if id == user['id']:
                    if user['role'] == 'admin':
                        return_user = user
                    else:
                        if user['activated']:
                            return_user = user

            return_user['username'] = request.json['username']

            return make_response((return_user, 200))
        else:
            return {'error': 'Server Error'}, 500


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        error = None
        error_code = None
        global login_data
        global user_data

        if login_data:
            for user_login in login_data:
                if user_login['username'] == request.json['username']:
                    error_code = 409
                    error = 'Username already exists!'

            for user in user_data:
                if user['email'] == request.json['email']:
                    error_code = 409
                    error = 'Email already exists!'
                if user['mobile'] == request.json['mobile']:
                    error_code = 409
                    error = 'Mobile number already exists'

        if not error_code:
            id = login_data[-1]['id'] + 1

            new_user_login = {
                'id': id,
                'username': request.json['username'],
                'password': request.json['password']
            }

            new_user = {
                'id': id,
                'fullname': request.json['fullname'],
                'email': request.json['email'],
                'mobile': request.json['mobile'],
                'role': "normal",
                'activated': False
            }

            login_data.append(new_user_login)
            user_data.append(new_user)

            return '', 204

        if error_code:
            return {'error': error}, error_code


@bp.route('/admin-delete-user/', methods=('GET', 'DELETE'))
def admin_delete_user():
    if request.method == 'DELETE':
        error = None
        error_code = None
        id = int(request.args.get('id'))
        userid = int(request.args.get('userid'))
        global user_data
        global login_data

        if id == 0 != userid:
            new_user_data = []

            for user in user_data:
                if user['id'] != userid:
                    new_user_data.append(user)

            new_login_data = []
            for user_login in login_data:
                if user_login['id'] != userid:
                    new_login_data.append(user_login)

            user_data = new_user_data
            login_data = new_login_data

        else:
            error = 'You are trying to delete yourself!'
            error_code = 409

        if error:
            return {'error': error}, error_code
        else:
            return '', 204


@bp.route('/add-subordinate', methods=('GET', 'PUT'))
def add_subordinate():
    if request.method == 'PUT':
        id = request.json['id']
        userid = request.json['userid']
        global user_subordinate
        global user_data

        for user_sub in user_subordinate:
            if user_sub['id'] == id and userid == user_sub['subordinate_id']:
                return {'error': 'already a subordinate!'}, 409

        for user in user_data:
            if (user['id'] == id or user['id'] == userid) and not user['activated']:
                return {'error': 'user not activated!'}, 409

        user_subordinate.append({
            'id': id,
            'subordinate_id': userid
        })

        return '', 204


@bp.route('/remove-subordinate/', methods=('GET', 'DELETE'))
def remove_subordinate():
    if request.method == 'DELETE':
        id = int(request.args.get('id'))
        userid = int(request.args.get('userid'))
        global user_data
        global user_subordinate

        for user in user_data:
            if (user['id'] == id or user['id'] == userid) and not user['activated']:
                return {'error': 'user not activated!'}, 409

        found = False
        new_sub = []
        for user_sub in user_subordinate:
            if user_sub['id'] == id and user_sub['subordinate_id'] == userid:
                found = True
            else:
                new_sub.append(user_sub)

        if found:
            user_subordinate = new_sub
            return '', 204
        else:
            return {'error': 'not a subordinate in the first place'}, 409


@bp.route('/update-user', methods=('GET', 'PUT'))
def update_user():
    if request.method == 'PUT':
        userid = request.json['userid']
        val = request.json['val']
        which = request.json['which']
        global user_data

        if len(user_data) > 0:

            for user in user_data:
                if user[which] == val:
                    return {'error': f'This {which} is already being used!'}, 409

            _update_user_data = []

            for user in user_data:
                each_user = user
                if user['id'] == userid:
                    each_user[which] = val

                _update_user_data.append(each_user)

            user_data = _update_user_data
            return '', 204
        else:
            return {'error': 'no user detected'}, 409

