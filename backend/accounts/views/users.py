from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from rest_framework import permissions
from ._base_imports import *

from accounts.models.users import CustomUser
from accounts.serializers.users import CustomUserSerializer

from accounts.selectors.users import *


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_interns(self, request):
        supervisor = request.user
        if not supervisor.account_type == "supervisor":
            return Response(
                {"detail": "You are not a supervisor"}, status=status.HTTP_403_FORBIDDEN
            )

        queryset = get_interns_by_supervisor(supervisor.id)
        serializer = self.get_serializer(queryset, many=True)
        interns = serializer.data

        for intern in interns:
            set_department(intern)
            set_supervisor(intern)
            set_intern_school(intern)
            set_mentor(intern)

        return Response(interns, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user = serializer.data

        user_info(user)

        return Response(user)


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        context = {"detail": "Registration successful. Please login"}
        return Response(context, status=status.HTTP_201_CREATED)


class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise AuthenticationFailed("Missing required login credential")

        user = get_user_by_username(username)

        if not user:
            context = {
                "detail": "Invalid Student ID",
                "errors": {"Username": [f"no account found for '{username}'"]},
            }
            raise NotFound(context)

        if user.check_password(password) and user.is_active:
            # generate token for user
            token = RefreshToken.for_user(user)
            user_data = user_info(user)
            context = {
                "detail": "Login successful",
                "user": user_data,
                "token": {"access": str(token.access_token), "refresh": str(token)},
            }
            return Response(context, status=status.HTTP_200_OK)

        raise AuthenticationFailed("Incorrect login credentials provided")
