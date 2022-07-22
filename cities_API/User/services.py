from djoser.serializers import UserSerializer


def jwt_response_payload_handler(_, user=None, request=None):
    user = UserSerializer(user, context={'request': request}).data
    return {
        'userid': user['id'],
    }
