from rest_framework import serializers

from submissions.models.portfolios import PortfolioFile, PortfolioImage
from submissions.utils.helpers import absolute_media_url_builder

class PortfolioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = absolute_media_url_builder(
            self.context["request"], instance.image.url
        )
        return data


class PortfolioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioFile
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["file"] = absolute_media_url_builder(
            self.context["request"], instance.file.url
        )
        return data
