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
        for card_detail in card_details:
            if len(card_detail.get('offers')) < 1:
                continue
            for offer in card_detail.get('offers'):
                if not offer.get('cash_back_percentage'):
                    continue

                # check if the offer is expired
                date_time = datetime.datetime.now(pytz.timezone(app_variables.get('default_timezone')))
                if offer.get('expiry_date') and \
                        offer.get('expiry_date') < date_time.isoformat():
                    continue
                details = {
                    "name": card_detail.get('name'),
                    "company_name": card_detail.get('company_name'),
                    "offer": offer
                }

                category = offer.get('category')
                if not result.get(category):
                    result[category] = details
                else:
                    if result.get(category).get('offer').get('cash_back_percentage') < \
                            offer.get('cash_back_percentage'):
                        result[category] = details

        return JsonResponder().return_json_data(200, "SUCCESS", result)
