from rest_framework import serializers


from submissions.models.submissions import Comment
from accounts.serializers.users import UserAccountSerializer as SupervisorSerializer
from accounts.models.users import UserAccount


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = (
            SupervisorSerializer(instance.supervisor).data
            if instance.supervisor
            else None
        )
        return data
