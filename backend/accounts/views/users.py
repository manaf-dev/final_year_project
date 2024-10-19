from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from dj_rest_auth.registration.views import RegisterView

from accounts.selectors.users import get_users
from accounts.serializers.users import CustomUserSerializer


class CustomRegisterView(RegisterView):
    def get_response_data(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return {
            "key": token.key,
        }


@api_view(["GET"])
def list_users(request):
    users = get_users()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)
