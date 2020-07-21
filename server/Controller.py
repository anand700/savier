# Responsibilities:
# 1. Routes to either user service or search service.
# 2. Validates Token
# 3. Passes the request json to service.

from flask import Flask, request, jsonify
import jwt
from functools import wraps
import server.Service.UserService
from flask_cors import CORS, cross_origin
import base64
from flask_mail import Mail, Message
import os
import json

app = Flask(__name__)

# Todo: RELEASE: Change the SERVER_URL before and after release.
site_root = os.path.realpath(os.path.dirname(__file__))
# Main
# json_url = os.path.join(site_root, "setup", "config.json")
# localhost laptop
json_url = os.path.join(site_root, "setup", "config_localhost_laptop.json")

with open(json_url, 'r') as f:
    configuration = json.load(f)
    app.config.update(configuration)

mail = Mail(app)


def custom_token_required(f):
    """

    :param f:
    :return:
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)
        token = None
        if 'Authorization' in request.headers:
            token = base64.b64decode(request.headers['Authorization'])
        if not token:
            return jsonify({'message': "Token is required!", 'status': 401, 'data': ""})
        app.logger.info(app.config['SECRET_KEY'], token.decode("utf-8"))
        if app.config['SECRET_KEY'] != token.decode("utf-8"):
            return jsonify({'message': "Token is invalid.", 'status': 401, 'data': ""})

        return f(*args, **kwargs)

    return decorated


def token_required(f):
    """

    :param f:
    :return:
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)

        try:
            token = None
            if 'Authorization' in request.headers:
                token = base64.b64decode(request.headers['Authorization'])
            if not token:
                return jsonify({'message': "Token is required!", 'status': 401, 'data': ""})

            data = jwt.decode(token, app.config['SECRET_KEY'], options={'verify_exp': False})
            user_service = server.Service.UserService.UserService
            current_user = user_service().get_user_details_for_public_id(app, data['public_id'])
            if not current_user:
                return jsonify({'message': "Token is invalid.", 'status': 401, 'data': ""})
        except jwt.InvalidTokenError:
            return jsonify({'message': "Token is invalid.", 'status': 401, 'data': ""})

        return f(current_user, *args, **kwargs)

    return decorated


def login_validation(f):
    """

    :param f:
    :return:
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)

        try:
            token = None
            auth = dict()
            if 'Authorization' in request.headers:
                token = base64.b64decode(request.headers['Authorization'])
                token_split = token.decode("utf-8").split(":")
                auth['username'] = base64.b64decode(token_split[0]).decode("utf-8")
                auth['password'] = base64.b64decode(token_split[1]).decode("utf-8")
            if not token:
                return jsonify({'message': "Username or Password is incorrect.", 'status': 401, 'data': ""})
            if not auth:
                return jsonify({'message': "Username or Password is incorrect.", 'status': 401, 'data': ""})
        except Exception:
            return jsonify({'message': "Username or Password is incorrect.", 'status': 401, 'data': ""})

        return f(auth, *args, **kwargs)

    return decorated


@app.route('/v1/users', methods=['POST'])
@custom_token_required
@cross_origin(origin='*')
def create_user():
    """

    :return:
    """
    #  To create a user you need to know a secret key which
    #  is verified in the backend. This is to avoid people adding a user randomly.
    #  This method creates a user.
    user_service = server.Service.UserService.UserService
    return user_service().create_user(app, request.get_json())


@app.route('/v1/users/login', methods=['POST'])
@login_validation
@cross_origin(origin='*')
def user_login(auth):
    """

    :return:user details
    """
    #  Used to login a User where token and last modified fields are updated.
    #  UI - User
    user_service = server.Service.UserService.UserService
    return user_service().user_login(app, auth)


@app.route('/v1/users/logout', methods=['POST'])
@token_required
@cross_origin(origin='*')
def user_logout(current_user):
    """

    :param current_user:
    :return True or False:
    """
    #  This API is used to logout a user.
    #  UI - USER
    user_service = server.Service.UserService.UserService
    return user_service().user_logout(app, current_user)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, threaded=True, host="0.0.0.0", port=port, use_reloader=False)
