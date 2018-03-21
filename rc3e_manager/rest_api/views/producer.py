from rest_framework import generics

from rc3e_manager.backend.models import Producer
from rc3e_manager.rest_api.serializers import ProducerSerializer


class ProducerList(generics.ListCreateAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer


class ProducerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
