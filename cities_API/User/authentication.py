from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework_simplejwt.settings import api_settings

from rest_framework.authentication import TokenAuthentication

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES


class CustomKeywordAuth(TokenAuthentication):
    keyword = 'JWT'


class JWTCookieAuthMixin:
    """Make JWT retrieve token from cookies"""
    def authenticate(self, request):
        access_token = request.COOKIES.get('Authorization')
        if(access_token):
            request.META['HTTP_AUTHORIZATION'] = '{header_type} {access_token}'.format(
                header_type=settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0], access_token=access_token)

        return super().authenticate(request)

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )


class CustomCookieBasedAuthentication(JWTCookieAuthMixin, JWTAuthentication):
    """Auth based on JWT token stored in cookies"""
    pass