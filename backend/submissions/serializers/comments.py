from rest_framework import serializers


from submissions.models.submissions import Comment
from accounts.serializers.users import SupervisorSerializer
from accounts.models.users import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    author = SupervisorSerializer(read_only=True)
    supervisor = serializers.PrimaryKeyRelatedField(
        source="author", queryset=CustomUser.objects.all(), write_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "author", "supervisor", "content", "submission", "updated_at")
