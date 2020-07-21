class User:
    user = {
        "app_data": {
            "username": "",
            "password": "",
            "email_address": "",
            "first_name": "",
            "last_name": "",
            "photo_url": "",
            "is_active": "",
            "last_modified": "",
            "create_date": "",
            "public_id": "",
            "user_type_id": "",
            "api_key_token": ""
        },
        "cards": [],
        "other": {
        }
    }

    def __init__(self, app_data, cards, other):

        # app data
        if app_data:
            self.user['app_data']['username'] = app_data.get('username')
            self.user['app_data']['password'] = app_data.get('password')
            self.user['app_data']['email_address'] = app_data.get('email_address')
            self.user['app_data']['first_name'] = app_data.get('first_name')
            self.user['app_data']['last_name'] = app_data.get('last_name')
            self.user['app_data']['photo_url'] = app_data.get('photo_url')
            self.user['app_data']['is_active'] = app_data.get('is_active')
            self.user['app_data']['last_modified'] = app_data.get('last_modified')
            self.user['app_data']['create_date'] = app_data.get('create_date')
            self.user['app_data']['public_id'] = app_data.get('public_id')
            self.user['app_data']['user_type_id'] = app_data.get('user_type_id')
            self.user['app_data']['api_key_token'] = app_data.get('api_key_token')

        if cards:
            self.user['cards'] = cards

        if other:
            self.user['other'] = other

    def print_user(self):
        print("app_data  = " + str(self.user['app_data']))
        print("cards  = " + str(self.user['cards']))
        print("other = " + str(self.user['other']))
