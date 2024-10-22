from rest_framework import serializers

from submissions.models.portfolios import PortfolioFile, PortfolioImage


class PortfolioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = "__all__"


class PortfolioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioFile
        fields = "__all__"
