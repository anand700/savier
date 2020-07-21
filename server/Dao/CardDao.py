import datetime
import pytz

from flask_pymongo import PyMongo
from bson.objectid import ObjectId


class CardDao:
    # Responsibilities:
    # 1. Calls the database using database connector.

    def __init__(self):
        pass

    @classmethod
    def get_card_details(cls, app, query, response_without):

        response = []

        try:
            database = PyMongo(app)
            result = database.db.card_details.find(query, response_without)

            for each_value in result:
                response.append(each_value)

        except:
            app.logger.error(" CardDao : "
                             "get_card_details() ")

        return response
