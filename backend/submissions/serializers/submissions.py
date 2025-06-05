from rest_framework import serializers

from accounts.models.users import UserAccount
from submissions.models.submissions import Submission, SubmissionVideo
from accounts.serializers.users import UserAccountSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class SubmissionVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionVideo
        fields = "__all__"

    def validate(self, attrs):
        video_url = attrs.get("video_url")
        if video_url:
            validator = URLValidator()
            try:
                validator(video_url)
            except ValidationError:
                raise serializers.ValidationError({"video_url": "Enter a valid URL."})
        return attrs


class SubmissionSerializer(serializers.ModelSerializer):
    # intern = UserAccountSerializer(read_only=True)
    # intern_source = serializers.PrimaryKeyRelatedField(
    #     source="intern", queryset=UserAccount.objects.all(), write_only=True
    # )

    class Meta:
        model = Submission
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["intern"] = UserAccountSerializer(instance.intern).data
        try:
            if instance.video:
                data["video"] = SubmissionVideoSerializer(instance.video).data
        except:
            return data

        return data
