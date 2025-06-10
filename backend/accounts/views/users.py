from ._base_imports import *
from django.utils import timezone
from rest_framework.exceptions import NotFound, NotAcceptable, AuthenticationFailed
from accounts.serializers.users import UserAccountSerializer

from accounts.selectors.users import *
from accounts.services.users import create_user
from accounts.utils.emails import password_reset_email, password_reset_success_email
from accounts.utils.general import (
    get_password_reset_token,
    decrypt_token,
    validate_posted_data,
    get_user_from_jwttoken,
)
from internships.selectors import get_cohort_by_year


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["register_intern", "list_supervisors"]:
            self.permission_classes = [permissions.AllowAny]

        return super().get_permissions()

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        context = user_representation(instance)
        return Response(context, status=status.HTTP_200_OK)

    def list_supervisors(self, request):
        """
        List all supervisors in the system
        """
        supervisors = get_supervisors()
        # context = user_representation(supervisors, many=True)
        return Response(supervisors, status=status.HTTP_200_OK)

    def _is_supervisor(self, request):
        supervisor = request.user

        if supervisor.account_type != "supervisor":
            return Response(
                {"detail": "You cannot perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return supervisor

    def get_cohort_interns(self, request, year):
        supervisor = self._is_supervisor(request)
        cohort = get_cohort_by_year(year=year)
        supervisor_interns = get_supervisor_interns_by_cohort(supervisor.id, cohort.id)
        interns = user_representation(supervisor_interns, many=True)
        context = {"interns": interns, "interns_count": supervisor_interns.count()}
        return Response(context, status=status.HTTP_200_OK)

    # def get_cohort_interns_count(self, request, year):
    #     supervisor = self._is_supervisor(request)
    #     cohort = get_cohort_by_year(year=year)

    #     supervisor_interns = get_interns_by_supervisor(supervisor.id)
    #     interns_count = supervisor_interns.filter(cohort=cohort).count()
    #     context = {"cohort": cohort.year, "interns_count": interns_count}
    #     return Response(context, status=status.HTTP_200_OK)

    def register_intern(self, request):
        data = request.data
        err, errors = validate_posted_data(
            data,
            [
                "username",
                "email",
                "password",
                "title",
                "first_name",
                "last_name",
                "phone",
                "department",
                "supervisor",
            ],
        )
        if err:
            return Response(
                {"detail": "missing required data", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if data.get("username") and not data.get("username").isnumeric():
            context = {
                "detail": "Invalid student ID",
                "errors": {"username": ["Student ID must be numeric"]},
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if UserAccount.objects.filter(email=data.get("email")).exists():
            context = {
                "detail": "Student with this Email already exists",
                "errors": {"email": [f"'{data.get('email')}' already registered"]},
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if UserAccount.objects.filter(username=data.get("username")).exists():
            context = {
                "detail": "Student with this ID already exists",
                "errors": {
                    "username": [f"'{data.get('student id')}' already registered"]
                },
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if not UserAccount.objects.filter(id=data.get("supervisor")).exists():
            context = {
                "detail": "Supervisor not found",
                "errors": {"supervisor": ["Supervisor does not exist"]},
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        cohort = get_cohort_by_year(year=timezone.now().year)
        if not cohort:
            context = {
                "detail": "No active cohort found for this year",
                "errors": {"cohort": ["No active cohort for this year"]},
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        data["cohort"] = cohort.id
        data["level"] = "400"
        data["account_type"] = "intern"
        data["supervisor"] = data.get("supervisor")

        user_data, errors = create_user(data)
        if errors:
            context = {"detail": "Error creating user", "errors": errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_by_email(user_data.get("email"))
        user.set_password(data.get("password"))
        user.save()
        return Response(
            {"detail": "Intern registered successfully, please login"},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
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
                "detail": "Invalid credentials",
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

            user_data = user_representation(user)
            context = {
                "detail": "Login successful",
                "user": user_data,
                "token": {"access": str(token.access_token), "refresh": str(token)},
            }
            return Response(context, status=status.HTTP_200_OK)

        raise NotFound("Invalid credentials")


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

    def change_password(self, request):
        """Change password for a user account"""
        user = get_user_from_jwttoken(request)
        if not user:
            context = {"detail": "Authorization header is required"}
            raise AuthenticationFailed(context)

        err, errors = validate_posted_data(
            request.data, ["current_password", "password"]
        )
        if err:
            return Response(
                {"detail": "missing required data", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_password = request.data.get("current_password")
        password = request.data.get("password")

        if not user.check_password(current_password):
            context = {"detail": "incorrect current password"}
            raise NotAcceptable(context)

        user.set_password(password)
        user.save()

        context = {"detail": "Password successfully changed"}
        return Response(context, status.HTTP_200_OK)
