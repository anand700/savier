import datetime
import pytz

from flask_pymongo import PyMongo
from bson.objectid import ObjectId


class UserDao:
    # Responsibilities:
    # 1. Calls the database using database connector.

    date_format = '%Y-%m-%d %H:%M:%S'
    DB_TIMEZONE = "UTC"

    def __init__(self):
        pass

    @classmethod
    def create_user(cls, app, user_dict):

        result = []

        try:
            database = PyMongo(app)
            user_dict['_id'] = ObjectId()
            result = database.db.users.insert(user_dict)

        except:
            app.logger.error(" UserDao : "
                             "create_user() ")

        if result:
            return True
        else:
            return False

    @classmethod
    def get_user_fields_for_username(cls, app, auth):

        result = []

        try:
            database = PyMongo(app)
            result = database.db.users.find_one(
                {
                    'app_data.username': auth['username'],
                    'app_data.is_active': 'Y'
                }, {"_id": 0})

        except:
            app.logger.error(" UserDao : "
                             "get_user_fields_for_username() ")

        return result

    @classmethod
    def update_token(cls, app, user_public_id, token):

        result = []

        try:
            database = PyMongo(app)
            result = database.db.users.update({'app_data.public_id': user_public_id},
                                             {
                                                 "$set": {
                                                     'app_data.api_key_token': token,
                                                     'app_data.last_modified': datetime.datetime.now(
                                                         pytz.timezone(cls.DB_TIMEZONE))
                                                 }
                                             })

        except:
            app.logger.error(" UserDao : "
                             "update_token() ")

        return result

    @classmethod
    def does_username_exist(cls, app, username):

        result = []

        try:
            database = PyMongo(app)
            result = database.db.users.find_one({'app_data.username': username}, {"_id": 0})

        except:
            app.logger.error(" UserDao : "
                             "does_username_exist() ")

        return result

    @classmethod
    def does_email_exist(cls, app, email_address):

        result = []

        try:
            database = PyMongo(app)
            result = database.db.users.find_one({'app_data.email_address': email_address}, {"_id": 0})

        except:
            app.logger.error(" UserDao : "
                             "does_email_exist() ")

        return result

    @classmethod
    def user_logout(cls, app, current_user):

        result = []

        try:
            database = PyMongo(app)
            result = database.db.users.update({'app_data.public_id': current_user['app_data']['public_id']},
                                             {"$set": {'app_data.api_key_token': ''}})

        except:
            app.logger.error(" UserDao : "
                             "user_logout() ")

        if result:
            return True
        else:
            return False

    @classmethod
    def get_user_details_for_public_id(cls, app, public_id, response_without):

        result = []

        try:
            database = PyMongo(app)
            result = database.db.users.find_one(
                {
                    'app_data.public_id': public_id,
                    'app_data.is_active': 'Y'
                }, response_without)

        except:
            app.logger.error(" UserDao : "
                             "get_user_details_for_public_id() ")
        return result

    @classmethod
    def get_all_users(cls, app, response_without):

        response = []

        try:
            database = PyMongo(app)
            result = database.db.users.find(
                {
                    'app_data.is_active': 'Y'
                }, response_without).limit(1000)

            for each_value in result:
                response.append(each_value)

        except:
            app.logger.error(" UserDao : "
                             "get_all_users() ")

        return response
