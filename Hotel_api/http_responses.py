from enum import Enum

from enum import Enum

class HTTPResponse(Enum):
    _OK = 200
    _CREATED = 201
    _ACCEPTED = 202
    _NO_CONTENT = 204
    _BAD_REQUEST = 400
    _UNAUTHORIZED = 401
    _NOT_FOUND = 404
    _INTERNAL_SERVER_ERROR = 500
    # Add more responses as needed

    @staticmethod
    def OK():
        return HTTPResponse._OK.value

    @staticmethod
    def CREATED():
        return HTTPResponse._CREATED.value
    
    @staticmethod
    def ACCEPTED():
        return HTTPResponse._ACCEPTED.value

    @staticmethod
    def NO_CONTENT():
        return HTTPResponse._NO_CONTENT.value

    @staticmethod
    def BAD_REQUEST():
        return HTTPResponse._BAD_REQUEST.value

    @staticmethod
    def UNAUTHORIZED():
        return HTTPResponse._UNAUTHORIZED.value

    @staticmethod
    def NOT_FOUND():
        return HTTPResponse._NOT_FOUND.value

    @staticmethod
    def INTERNAL_SERVER_ERROR():
        return HTTPResponse._INTERNAL_SERVER_ERROR.value
    
from enum import Enum

class HTTPResponseText(Enum):
    _200 = 'OK'
    _201 = 'Created'
    _202  = 'Accepted'
    _204 = 'No Content'
    _400 = 'Bad Request'
    _401 = 'Unauthorized'
    _403 = 'Forbidden'
    _404 = 'Not Found'
    _500 = 'Internal Server Error'
    # Add more responses as needed

    @staticmethod
    def OK():
        return HTTPResponseText._200.value

    @staticmethod
    def CREATED():
        return HTTPResponseText._201.value
    
    @staticmethod
    def ACCEPTED():
        return HTTPResponseText._201.value

    @staticmethod
    def NO_CONTENT():
        return HTTPResponseText._204.value

    @staticmethod
    def BAD_REQUEST():
        return HTTPResponseText._400.value

    @staticmethod
    def UNAUTHORIZED():
        return HTTPResponseText._401.value

    @staticmethod
    def FORBIDDEN():
        return HTTPResponseText._403.value

    @staticmethod
    def INTERNAL_SERVER_ERROR():
        return HTTPResponseText._500.value
    
    @staticmethod
    def NOT_FOUND():
        return HTTPResponseText._404.value
