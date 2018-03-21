"""rc3e_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rc3e_manager import views
from rc3e_manager.rest_api import urls as rest_urls
from rc3e_manager.web_api import urls as web_urls

app_name = 'rc3e_manager'

admin.autodiscover()

urlpatterns = [
    # General views
    url(r'^$', views.welcome, name="welcome"),
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^web_api/', include(web_urls)),
    url(r'^rest_api/', include(rest_urls))
]
