import pytz
import jwt
import datetime
import json
import uuid
import base64

from server.Dao.UserDao import UserDao
from server.Service.JsonResponder import JsonResponder
from validate_email import validate_email
from server.Service.User import User
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class UserService:
    # Responsibilities:
    # 1. Does all the validations required to process the API. This includes email and phone number validation.
    # 2. Responsible for returning json format data(this includes error messages, fetching all rows)
    #  to the UI using JsonResponder class.

    def __init__(self):
        pass

    @classmethod
    def create_user(cls, app, json_input):
        """

        :param app:
        :param json_input:
        :return:
        """
        user_dao = UserDao

        # convert json to dict
        user_dict = json.loads(json.dumps(json_input))

        # password
        password = base64.b64decode(user_dict.get('app_data').get('password'))

        # Validations
        if not user_dict.get('app_data').get('username').strip():
            return JsonResponder().return_json_data(400, "USERNAME_REQUIRED", "")
        if user_dao().does_username_exist(app, user_dict.get('app_data').get('username').strip()):
            return JsonResponder().return_json_data(400, "USERNAME_EXISTS", "")
        if not password:
            return JsonResponder().return_json_data(400, "PASSWORD_REQUIRED", "")
        if not user_dict.get('app_data').get('email_address').strip():
            return JsonResponder().return_json_data(400, "EMAIL_ADDRESS_REQUIRED", "")
        if not validate_email(user_dict.get('app_data').get('email_address').strip()):
            return JsonResponder().return_json_data(400, "EMAIL_ADDRESS_NOT_VALID", "")
        if user_dao().does_email_exist(app, user_dict.get('app_data').get('email_address').strip()):
            return JsonResponder().return_json_data(400, "USER_EMAIL_EXISTS", "")
        if not user_dict.get('app_data').get('first_name').strip():
            return JsonResponder().return_json_data(400, "FIRST_NAME_REQUIRED", "")
        if not user_dict.get('app_data').get('last_name').strip():
            return JsonResponder().return_json_data(400, "LAST_NAME_REQUIRED", "")

        app_variables = app.config['APP_VARIABLES']
        user_dict['app_data']['user_type_id'] = app_variables.get('user_type_id')
        user_dict['app_data']['is_active'] = "Y"
        user_dict['app_data']['create_date'] = datetime.datetime.now(pytz.timezone(app_variables.get('db_timezone')))
        user_dict['app_data']['last_modified'] = datetime.datetime.now(pytz.timezone(app_variables.get('db_timezone')))
        user_dict['app_data']['public_id'] = str(uuid.uuid4())

        # Generate a sha256 encoded password #
        hashed_password = generate_password_hash(password, method='sha256')
        user_dict['app_data']['password'] = hashed_password
        user = User(
            user_dict.get('app_data'),
            user_dict.get('cards'),
            user_dict.get('other')
        )

        res = user_dao().create_user(app, user.user)
        return JsonResponder().return_json_data(200, "SUCCESS", res)

    @classmethod
    def user_login(cls, app, auth):
        """

        :param app:
        :param auth:
        :return:
        """
        user_dao = UserDao

        # Validations before
        if not auth:
            return JsonResponder().return_json_data(400, "USERNAME_OR_PASSWORD_INCORRECT", "")
        if not auth['username']:
            return JsonResponder().return_json_data(400, "USERNAME_REQUIRED", "")
        if not auth['password']:
            return JsonResponder().return_json_data(400, "PASSWORD_REQUIRED", "")

        user = user_dao().get_user_fields_for_username(app, auth)
        app_variables = app.config['APP_VARIABLES']

        # Validations after
        if not user:
            return JsonResponder().return_json_data(400, "USERNAME_OR_PASSWORD_INCORRECT", "")
        if not check_password_hash(user['app_data']['password'], auth['password']):
            return JsonResponder().return_json_data(400, "USERNAME_OR_PASSWORD_INCORRECT", "")
        if user['app_data']['user_type_id'] != app_variables.get('user_type_id'):
            return JsonResponder().return_json_data(401, "NOT_USER_LOGIN", "")

        token = jwt.encode(
            {
                'public_id': user['app_data']['public_id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            app.config['SECRET_KEY']
        )
        update_token_res = user_dao().update_token(
            app,
            user['app_data']['public_id'],
            token.decode('UTF-8')
        )

        if not update_token_res:
            return JsonResponder().return_json_data(500, "", "")

        del user['app_data']['api_key_token']
        del user['app_data']['password']
        del user['app_data']['user_type_id']
        user['app_data']['api_key_token'] = token.decode('UTF-8')

        return JsonResponder().return_json_data(200, "SUCCESS", user)

    @classmethod
    def user_logout(cls, app, current_user):
        """

        :param app:
        :param current_user:
        :return:
        """
        user_dao = UserDao
        app_variables = app.config['APP_VARIABLES']

        if current_user['app_data']['user_type_id'] != app_variables.get('user_type_id'):
            return JsonResponder().return_json_data(401, "NOT_USER_LOGIN", "")

        user_logout_res = user_dao().user_logout(app, current_user)
        if not user_logout_res:
            return JsonResponder().return_json_data(500, "", "")
        return JsonResponder().return_json_data(200, "SUCCESS", user_logout_res)

    @classmethod
    def get_user_details_for_public_id(cls, app, public_id):
        """

        :param app:
        :param public_id:
        :return:
        """
        user_dao = UserDao
        response_without = {
            "_id": 0
        }
        return user_dao().get_user_details_for_public_id(app, public_id, response_without)

    @classmethod
    def check_if_date_valid(cls, year, month, day):
        try:
            new_date = datetime.datetime(year, month, day)
            if new_date:
                res = True
            else:
                res = False
        except ValueError:
            res = False
        return res
