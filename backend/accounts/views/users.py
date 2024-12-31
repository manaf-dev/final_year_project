from dj_rest_auth.registration.views import RegisterView
from ._base_imports import *
from django.utils import timezone

from accounts.models.users import CustomUser
from accounts.serializers.users import CustomUserSerializer

from accounts.selectors.users import *
from accounts.selectors.intern_schools import get_intern_school_by_id


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

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

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        data = user_info(instance)
        user_data = data
        return Response({"user": user_data}, status=status.HTTP_200_OK)

    @action(methods=["patch"], detail=True)
    def update_school(self, request, pk=None):
        # print(request.data)
        intern_school = get_intern_school_by_id(request.data.get("id"))

        if not intern_school:
            return Response(
                {"detail": "School not found"}, status=status.HTTP_404_NOT_FOUND
            )

        instance = self.get_object()
        instance.intern_school = intern_school
        instance.save()
        serializer = self.get_serializer(instance)
        context = {
            "user": serializer.data,
            "detail": "Internship school added successful",
        }
        return Response(context, status=status.HTTP_200_OK)

    def check_supervisor(self, request):
        supervisor = request.user

        if supervisor.account_type != "supervisor":
            return Response(
                {"detail": "You cannot perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return supervisor

    def get_current_cohort_interns(self, request):
        supervisor = self.check_supervisor(request)
        current_year = timezone.now().year

        supervisor_interns = get_interns_by_supervisor(supervisor.id)
        current_cohort_interns = supervisor_interns.filter(cohort=str(current_year))

        interns_data = self.get_serializer(supervisor_interns, many=True).data

        return Response(interns_data, status=status.HTTP_200_OK)


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
            if user.account_type == "intern" and user.level != "400":
                context = {
                    "detail": f"You do not have access yet, level {user.level}",
                    "errors": {"Cohort": ["User level don't have access to system"]},
                }
                raise AuthenticationFailed(context)

            # generate token for user
            token = RefreshToken.for_user(user)
            user_data = user_info(user)
            context = {
                "detail": "Login successful",
                "user": user_data,
                "token": {"access": str(token.access_token), "refresh": str(token)},
            }
            return Response(context, status=status.HTTP_200_OK)

        raise AuthenticationFailed("Incorrect password")
