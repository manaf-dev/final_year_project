from rest_framework import serializers

from accounts.models.users import CustomUser
from submissions.models.submissions import Submission
from accounts.serializers.users import CustomUserSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    intern = CustomUserSerializer(read_only=True)
    intern_source = serializers.PrimaryKeyRelatedField(
        source="intern", queryset=CustomUser.objects.all(), write_only=True
    )

    class Meta:
        model = Submission
        fields = ("id", "month", "grade", "graded", "intern", "intern_source")
