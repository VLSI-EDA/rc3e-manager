from django.conf.urls import include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rc3e_manager.rest_api.views import ProducerDetail
from rc3e_manager.rest_api.views import ProducerList
from rc3e_manager.rest_api.views import RegionTypeDetail
from rc3e_manager.rest_api.views import RegionTypeList

urlpatterns = [
    url(r'^producers/$', ProducerList.as_view()),
    url(r'^producers/(?P<pk>[0-9]+)/$', ProducerDetail.as_view()),

    url(r'^region_types/$', RegionTypeList.as_view()),
    url(r'^region_types/(?P<pk>[0-9]+)/$', RegionTypeDetail.as_view()),

    url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
