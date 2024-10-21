from rest_framework import serializers

from accounts.models.mentors import Mentor


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = "__all__"
