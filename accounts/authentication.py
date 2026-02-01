from __future__ import annotations

from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from .models import User


class UserJWTAuthentication(authentication.BaseAuthentication):
    """Custom JWT authentication tied to the accounts.User model."""
    keyword = "Bearer"

    def authenticate(self, request):
        """Validate a Bearer token and return (user, token) or raise."""
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].decode().lower() != self.keyword.lower():
            return None

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed("Invalid authorization header.")

        token = auth[1].decode()
        try:
            validated = AccessToken(token)
        except (InvalidToken, TokenError):
            raise exceptions.AuthenticationFailed("Invalid token.")

        user_id = validated.get("user_id")
        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid token payload.")

        user = User.objects.filter(id=user_id).first()
        if not user:
            raise exceptions.AuthenticationFailed("User not found.")

        return (user, validated)

    @staticmethod
    def create_access_token(user_id: str) -> AccessToken:
        """Create a short-lived access token containing the user id."""
        token = AccessToken()
        token["user_id"] = user_id
        token["iss"] = settings.SECRET_KEY
        return token
