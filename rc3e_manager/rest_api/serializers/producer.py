from rest_framework import serializers

from rc3e_manager.backend.models import Producer


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = "__all__"
