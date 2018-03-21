from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rc3e_manager.rest_api.views import ProducerDetail
from rc3e_manager.rest_api.views import ProducerList

urlpatterns = [
    url(r'^producers/$', ProducerList.as_view()),
    url(r'^producers/(?P<pk>[0-9]+)/$', ProducerDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
