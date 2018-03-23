from rest_framework import generics

from rc3e_manager.backend.models import RegionType
from rc3e_manager.rest_api.serializers import RegionTypeSerializer


class RegionTypeList(generics.ListCreateAPIView):
    queryset = RegionType.objects.all()
    serializer_class = RegionTypeSerializer


class RegionTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegionType.objects.all()
    serializer_class = RegionTypeSerializer
