from rest_framework import serializers

from rc3e_manager.backend.models import RegionType


class RegionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionType
        fields = "__all__"
