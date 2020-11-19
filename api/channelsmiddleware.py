from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from asgiref.sync import sync_to_async


class TokenAuthMiddleware:
    """Custom token auth middleware"""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

            jwt_auth_object = JWTAuthentication()
            validated_token = await sync_to_async(jwt_auth_object.get_validated_token)(token)
            scope['user'] = await sync_to_async(jwt_auth_object.get_user)(validated_token)
        except (KeyError, InvalidToken):
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)

