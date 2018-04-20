from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import ListView

from rc3e_manager.backend.models import Fpga, FpgaModel, Node, Producer, Programmer, RegionType, VFpga
from rc3e_manager.web_api import views
from rc3e_manager.web_api.urls.generators import generate_create_view
from rc3e_manager.web_api.urls.generators import generate_delete_view
from rc3e_manager.web_api.urls.generators import generate_list_view

urlpatterns = [

    # --- General purpose URLs ---
    url(r'^$', views.welcome, name="welcome"),
    url(r'^blank/$', views.blank, name="blank"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    # --- Node-related URLs ---
    generate_create_view(Node, True),
    generate_delete_view(Node, True),
    generate_list_view(Node, True),

    # --- Producer-related URLs ---
    generate_create_view(Producer, True),
    generate_delete_view(Producer, True),
    generate_list_view(Producer, True),

    # --- FPGA Model-related URLs ---
    generate_create_view(FpgaModel, True),
    generate_delete_view(FpgaModel, True),
    generate_list_view(FpgaModel, True),

    # --- FPGA related URLs ---
    url(r'^fpgas/create/$', views.create_fpga, name='create_fpga'),  # custom
    generate_delete_view(Fpga, True),
    generate_list_view(Fpga, True),

    url(r'^fpgas/show/(?P<pk>[\d]+)/$', views.show_fpga, name='show_fpga'),

    # --- Region Type related URLs ---
    generate_create_view(RegionType, True),
    generate_delete_view(RegionType, True),
    generate_list_view(RegionType, True),

    # --- Reservation related URLs ---

    url(r'^reservations/create',
        views.create_reservation,
        name='create_reservation'
        ),

    url(r'^reservations/list/',
        ListView.as_view(
            model=VFpga,
            context_object_name='object_list',
            template_name='reservations/list_vfpgas.html',
        ), name='list_vfpgas'),

    # --- Programmer related URLs ---
    generate_create_view(Programmer, True),
    generate_delete_view(Programmer, True),
    generate_list_view(Programmer, True),
]
