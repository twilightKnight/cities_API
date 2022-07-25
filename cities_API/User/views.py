import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView


class SetCookieMixin:
    """Store JWT token in cookies instead of request headers"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        expires = datetime.datetime.strftime(
            datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
            "%a, %d-%b-%Y %H:%M:%S GMT",
        )
        response.set_cookie('Authorization', serializer.validated_data['access'], expires=expires)
        return response


class Login(SetCookieMixin, TokenObtainPairView):
    """User Login class"""
    pass