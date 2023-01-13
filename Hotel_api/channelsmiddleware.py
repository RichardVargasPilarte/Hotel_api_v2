from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode
from django.conf import settings


@database_sync_to_async
def gUser(uid):
    """
    get_user from token
    """
    close_old_connections()
    print("buscando : " + str(uid))
    try:
        user = get_user_model().objects.get(id=uid)
        print(user.username)
        return user
    except Exception as e:
        print('error', e)
        return AnonymousUser()


class JWTChannelMiddleware:
    """
    Middleware which populates scope["user"] from a simple JWT.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # if "headers" in scope:
        #     headers = dict(scope["headers"])

        #     if b"authorization" in headers:
        #         token_name, token_key = headers[b"authorization"].split()

        #         if token_name == b"Bearer":
        #             tk = token_key.decode()
        #             print(tk)
        #             scope["user"] = await get_user(tk)
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        token = parse_qs(scope["query_string"].decode("utf8"))["access"][0]

        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(
                token, settings.SECRET_KEY, algorithms=["HS512"])
            print(decoded_data)
            # Will return a dictionary like -
            # {
            #     "token_type": "access",
            #     "exp": 1568770772,
            #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
            #     "user_id": 6
            # }

            # Get the user using ID
            print(decoded_data["user_id"])
            scope["user"] = gUser(decoded_data["user_id"])

        # Return the inner application directly and let it run everything else

        return await self.inner(scope, receive, send)  # linea de posible error
