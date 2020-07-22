import pytz
import jwt
import datetime
import json
import uuid
import base64

from server.Dao.UserDao import UserDao
from server.Dao.CardDao import CardDao
from server.Service.JsonResponder import JsonResponder
from validate_email import validate_email
from server.Service.User import User
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class CardService:
    # Responsibilities:
    # 1. Does all the validations required to process the API.
    # 2. Responsible for returning json format data(this includes error messages, fetching all rows)
    #  to the UI using JsonResponder class.

    def __init__(self):
        pass

    @classmethod
    def get_category_users_card_mapping(cls, app, current_user):
        """

        :param app:
        :param public_id:
        :return:
        """
        card_dao = CardDao
        response_without = {
            "_id": 0
        }

        query = {
            "name": {"$in": current_user.get('cards')}
        }

        card_details = card_dao().get_card_details(app, query, response_without)
        app_variables = app.config.get('APP_VARIABLES')

        result = {}
        for i in range(len(card_details)):
            if not card_details[i].get('offer') or not card_details[i].get('offer').get('category'):
                continue
            for category_type, offers in card_details[i].get('offer').get('category').items():
                for offer in offers:
                    if not offer.get('cash_back_percentage'):
                        continue

                    # check if the offer is expired
                    date_time = datetime.datetime.now(pytz.timezone(app_variables.get('default_timezone')))
                    if offer.get('expiry_date') and \
                            offer.get('expiry_date').strftime('%Y-%m-%d') < date_time.strftime('%Y-%m-%d'):
                        continue
                    details = {
                        "name": card_details[i].get('name'),
                        "company_name": card_details[i].get('company_name'),
                        "offer": offer
                    }
                    if not result.get(category_type):
                        result[category_type] = details
                    else:
                        if result.get(category_type).get('offer').get('cash_back_percentage') < \
                                offer.get('cash_back_percentage'):
                            result[category_type] = details

        return JsonResponder().return_json_data(200, "SUCCESS", result)
