from rest_framework import serializers

from submissions.models.submissions import Submission, Comment


class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
