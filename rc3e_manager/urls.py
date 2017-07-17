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

from fpga_manager import urls as fpga_manager_urls
from rc3e_manager import views

admin.autodiscover()

urlpatterns = [
    # General views
    url(r'^$', views.welcome, name="welcome"),
    url(r'^admin/', include(admin.site.urls)),
    # FPGA manager views
    url(r'^fpga_manager/', include(fpga_manager_urls)),
]
