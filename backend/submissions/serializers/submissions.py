from rest_framework import serializers

from submissions.models.submissions import Submission
from accounts.serializers.users import CustomUserSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    # intern = CustomUserSerializer()

    class Meta:
        model = Submission
        fields = ("id", "month", "grade", "graded", "intern")
