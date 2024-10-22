from ._base_imports import *

from accounts.models.mentors import Mentor


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = "__all__"
