from flask import request


def user_parse():
    data = request.get_json()
    dict = {
        'username': data.get('username'),
        'email': data.get('email'),
        'password': data.get('password'),
        'role': data.get('role')
    }

    return dict

