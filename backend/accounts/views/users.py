from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.selectors.users import get_users
from accounts.serializers.users import CustomUserSerializer
from accounts.models.users import CustomUser

class CustomUserListCreateAPIView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer





# @api_view(["GET"])
# def list_users(request):
#     users = get_users()
#     serializer = CustomUserSerializer(users, many=True)
#     return Response(serializer.data)
