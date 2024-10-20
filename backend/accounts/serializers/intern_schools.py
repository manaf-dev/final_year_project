from rest_framework import serializers

from accounts.models.intern_schools import InternSchool


class InternSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = InternSchool
        fields = "__all__"
