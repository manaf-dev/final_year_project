from dj_rest_auth.registration.serializers import RegisterSerializer
from ._base_imports import *

from accounts.models.users import CustomUser
from accounts.serializers.intern_schools import InternSchoolSerializer


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "supervisor_account",
            "intern_account",
            "department",
            "supervisor",
            "intern_school",
            "mentor",
        )


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    intern_account = serializers.BooleanField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        print(self.validated_data)
        data["first_name"] = self.validated_data.get("first_name", "")
        data["last_name"] = self.validated_data.get("last_name", "")
        data["intern_account"] = self.validated_data.get("intern_account", "")
        print(data)
        return data

    def save(self, request):
        user = super().save(request)
        user.intern_account = self.cleaned_data["intern_account"]
        user.save()
        return user
