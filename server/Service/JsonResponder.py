from flask import jsonify


class JsonResponder:
    # This class defines with json response for all api calls.
    # Call the method "return_json_data()" with parameters status,
    # message and data. if message is not defined it returns the
    # default message for a given status. #

    def __init__(self):
        self.__status = 200
        self.__data = ""
        self.__message = ""

    def custom_return_json_data(self, status=200, msg="", data=""):
        self.__status = status
        self.__data = data
        if not msg:
            self.__message = self.get_msg_for_status(status)
        elif msg:
            self.__message = msg
        return jsonify({'message': self.__message, 'status': self.__status, 'data': self.__data})

    def return_json_data(self, status=200, msg="", data=""):
        self.__status = status
        self.__data = data
        if not msg:
            self.__message = self.get_msg_for_status(status)
        elif msg:
            self.__message = self.get_msg(msg)
        return jsonify({'message': self.__message, 'status': self.__status, 'data': self.__data})

    @staticmethod
    def get_msg(msg):
        response_message = {
            'USERNAME_EXISTS': 'Username already exists.',
            'USERNAME_OR_PASSWORD_INCORRECT': 'Username or Password is incorrect.',
            'NOT_ADMIN_LOGIN': 'Not an Admin Login.',
            'NOT_USER_LOGIN': 'Not a User Login.',
            'USERNAME_REQUIRED': 'Username field is required.',
            'UNAUTHORIZED': 'Unauthorized.',
            'USER_ID_NOT_VALID': 'User Id not valid.',
            'ADDRESS1_FIELD_REQUIRED': 'Address1 field is required.',
            'CITY_FIELD_REQUIRED': 'City field is required.',
            'STATE_FIELD_REQUIRED': 'State field is required.',
            'ZIP_FIELD_REQUIRED': 'Zip field is required.',
            'USERNAME_NOT_VALID': 'Username not valid.',
            'PASSWORD_NOT_VALID': 'Password not valid.',
            'PASSWORD_REQUIRED': 'Password field is required.',
            'FIRST_NAME_NOT_VALID': 'First Name not valid',
            'LAST_NAME_NOT_VALID': 'Last Name not valid',
            'FIRST_NAME_REQUIRED': 'First Name field is required',
            'LAST_NAME_REQUIRED': 'Last Name field is required',
            'CONFIRM_PASSWORD_NOT_VALID': 'Confirm Password not valid.',
            'CONFIRM_PASSWORD_REQUIRED': 'Confirm Password field is required.',
            'PASSWORDS_DO_NOT_MATCH': 'Passwords do not match.',
            'EMAIL_ADDRESS_REQUIRED': 'Email Address field is required.',
            'EMAIL_ADDRESS_NOT_VALID': 'Email Address not valid.',
            'PHONE_NUMBER_NOT_VALID': 'Phone Number not valid.',
            'USERNAME_DOES_NOT_EXISTS': 'Username does not exist.',
            'USER_EMAIL_EXISTS': 'Email-Address already exists.',
            'SUCCESS': 'Success.',
            'NO_DATA_FOUND': 'No Data found.',
            'FAILED_TO_DELETE': 'Failed to Delete.',
            'FAILED_TO_UPDATE': 'Failed to Update.',
            'INTERNAL_SERVER_ERROR': 'Internal Server Error.',
            'FAILURE': 'Failed to retrieve data.',
            'ZIP_NOT_VALID': 'Zip not valid.',
            'USER_PUBLIC_ID_REQUIRED': 'User Public Id is required.',
            'NO_ACCESS_TO_BUILDINGS': 'Currently, you do not have access to any buildings.',
            'DATE_INVALID': 'Date is invalid.',
            'USER_PUBLIC_ID_NOT_VALID': 'User id is not valid.',
            'CITY_NOT_VALID': 'City not valid.',
            'STATE_NOT_VALID': 'State not valid.',
            'DB_HOST_REQUIRED': 'DB Host is required.',
            'ADDRESS1_NOT_VALID': 'Address1 not valid.',
            'PARAMETERS_NOT_VALID': 'Parameters not valid.',
            'DATE_REQUIRED': 'Date is required.',
            'USER_TYPE_NOT_VALID': 'User Type is not valid.',
        }
        return response_message[msg]

    @staticmethod
    def get_msg_for_status(status=200):
        status_message_mapping = {
            100: 'Continue',
            101: 'Switching Protocols',
            200: 'OK',
            201: 'Created',
            202: 'Accepted',
            203: 'Non-Authoritative Information',
            204: 'No Content',
            205: 'Reset Content',
            206: 'Partial Content',
            300: 'Multiple Choices',
            301: 'Moved Permanently',
            302: 'Found',
            303: 'See Other',
            304: 'Not Modified',
            305: 'Use Proxy',
            306: '(Unused)',
            307: 'Temporary Redirect',
            400: 'Bad Request',
            401: 'Unauthorized',
            402: 'Payment Required',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            406: 'Not Acceptable',
            407: 'Proxy Authentication Required',
            408: 'Request Timeout',
            409: 'Conflict',
            410: 'Gone',
            411: 'Length Required',
            412: 'Precondition Failed',
            413: 'Request Entity Too Large',
            414: 'Request-URI Too Long',
            415: 'Unsupported Media Type',
            416: 'Requested Range Not Satisfiable',
            417: 'Expectation Failed',
            500: 'Internal Server Error',
            501: 'Not Implemented',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Timeout',
            505: 'HTTP Version Not Supported'
        }
        return status_message_mapping[status]
