from rest_framework import serializers

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
            "school_mentor",
        )
