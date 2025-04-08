from ._base_imports import *
from django.utils import timezone
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.models import TokenModel

from accounts.models.users import CustomUser
from accounts.serializers.users import CustomUserSerializer

from accounts.selectors.users import *
from accounts.selectors.intern_schools import get_intern_school_by_id
from accounts.utils.emails import password_reset_email, password_reset_success_email
from accounts.utils.general import get_password_reset_token, decrypt_token

from internships.selectors import get_cohort_by_year


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        data = user_info(instance)
        user_data = data
        return Response({"user": user_data}, status=status.HTTP_200_OK)

    # @action(methods=["patch"], detail=True)
    # def update_school(self, request, pk=None):
    #     # print(request.data)
    #     intern_school = get_intern_school_by_id(request.data.get("id"))

    #     if not intern_school:
    #         return Response(
    #             {"detail": "School not found"}, status=status.HTTP_404_NOT_FOUND
    #         )

    #     instance = self.get_object()
    #     instance.intern_school = intern_school
    #     instance.save()
    #     serializer = self.get_serializer(instance)
    #     context = {
    #         "user": serializer.data,
    #         "detail": "Internship school added successful",
    #     }
    #     return Response(context, status=status.HTTP_200_OK)

    def check_supervisor(self, request):
        supervisor = request.user

        if supervisor.account_type != "supervisor":
            return Response(
                {"detail": "You cannot perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return supervisor

    def get_cohort_interns(self, request, year):
        supervisor = self.check_supervisor(request)
        cohort = get_cohort_by_year(year=year)

        supervisor_interns = get_interns_by_supervisor(supervisor.id)
        cohort_interns = supervisor_interns.filter(cohort=cohort)
        interns_data = self.get_serializer(cohort_interns, many=True).data

        return Response(interns_data, status=status.HTTP_200_OK)

    def get_cohort_interns_count(self, request, year):
        supervisor = self.check_supervisor(request)
        cohort = get_cohort_by_year(year=year)

        supervisor_interns = get_interns_by_supervisor(supervisor.id)
        interns_count = supervisor_interns.filter(cohort=cohort).count()
        context = {"cohort": cohort.year, "interns_count": interns_count}
        return Response(context, status=status.HTTP_200_OK)


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        context = {"detail": "Registration successful. Please login"}
        return Response(context, status=status.HTTP_201_CREATED)


class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username_or_email = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")

        if not username_or_email or not password:
            raise AuthenticationFailed("Missing required login credentials")

        if "@" in username_or_email:
            user = get_user_by_email(username_or_email)
        else:
            user = get_user_by_username(username_or_email)

        if not user:
            context = {
                "detail": "Incorrect username",
                "errors": {"Username": [f"no account found for '{username}'"]},
            }
            raise NotFound(context)

        if user.check_password(password) and user.is_active:
            if user.account_type == "intern" and user.level != "400":
                context = {
                    "detail": f"Level {user.level}, you do not have access",
                    "errors": {"Cohort": ["User level don't have access to system"]},
                }
                return Response(context, status=status.HTTP_403_FORBIDDEN)
            if user.account_type == "intern" and not user.supervisor:
                context = {
                    "detail": f"Supervisor not assigned to you yet. Try again later or visit IT directorate.",
                    "errors": {"Supervisor": ["User not assigned supervisor"]},
                }
                return Response(context, status=status.HTTP_403_FORBIDDEN)

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


class PasswordViewSet(viewsets.ViewSet):
    """Manages password change and reset"""

    permission_classes = [AllowAny]

    def request_token(self, request):
        """Request password reset token"""
        data = request.data
        user = get_user_by_email(data.get("email"))
        if not user:
            context = {
                "detail": "No account found",
                "errors": {"email": [f"no account exists for '{data.get('email')}' "]},
            }
            raise NotFound(context)

        email_thread = threading.Thread(
            target=password_reset_email, args=[user, user.email]
        )
        email_thread.start()

        context = {"detail": "Password reset verification token sent"}
        return Response(context, status.HTTP_200_OK)

    def reset_password(self, request, token):
        """
        Reset password for a user account
        """
        user_token = get_password_reset_token(decrypt_token(token))
        password = request.data.get("password")

        if not user_token:
            context = {
                "detail": "token not found",
                "errors": {"token": f"invalid token '{user_token.key}'"},
            }
            raise NotFound(context)

        if not password:
            return Response(
                {"detail": "Password field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_user_by_email(user_token.user.email)
        if not user:
            context = {
                "detail": "user not found",
                "errors": {"user": f"no account found"},
            }
            raise NotFound(context)

        user.set_password(password)
        user.save()
        user_token.delete()

        e_t = threading.Thread(
            target=password_reset_success_email, args=[user, user.email]
        )
        e_t.start()

        context = {"detail": "password reset successful"}
        return Response(context, status=status.HTTP_200_OK)

    # def change_password(self, request, user_id):
    #     """Change password for a user account"""
    #     current_password = request.data.get("current_password")
    #     password = request.data.get("password")

    #     err: bool = False
    #     errors: dict = {}
    #     if not current_password:
    #         err = True
    #         errors.update({"current_password": ["this field is required"]})
    #     if not password:
    #         err = True
    #         errors.update({"password": ["this field is required"]})

    #     if err:
    #         context = {"detail": "missing required data", "errors": errors}
    #         raise ValidationException(context)

    #     user = get_user_by_id(user_id)
    #     if not user:
    #         context = {
    #             "detail": "user not found",
    #             "errors": {
    #                 "email": [f"invalid pk'{user_id}' - object does not exist "]
    #             },
    #         }
    #         raise NotFound(context)

    #     if not user.check_password(current_password):
    #         context = {"detail": "incorrect current password"}
    #         raise NotAcceptable(context)

    #     user.set_password(password)
    #     user.save()

    #     context = {"detail": "password successfully changed"}
    #     return Response(context, status.HTTP_200_OK)
