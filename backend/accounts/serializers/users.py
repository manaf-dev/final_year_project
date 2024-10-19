from rest_framework import serializers

from accounts.models.users import CustomUser


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
            "school_mentor",
        )
