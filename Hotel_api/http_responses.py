from enum import Enum

class HTTPResponse(Enum):
    OK = (200, 'OK')
    CREATED = (201, 'Created')
    NO_CONTENT = (204, 'No Content')
    BAD_REQUEST = (400, 'Bad Request')
    UNAUTHORIZED = (401, 'Unauthorized')
    NOT_FOUND = (404, 'Not Found')
    INTERNAL_SERVER_ERROR = (500, 'Internal Server Error')
    # Add more responses as needed

    @classmethod
    def get_message(cls, code):
        for response in cls:
            if response.value[0] == code:
                return response.value[1]
        return None
