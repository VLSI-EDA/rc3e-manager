from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from fpga_manager import views
from fpga_manager.models import Fpga, FpgaModel, Node, Producer, RegionType

urlpatterns = [

    # TODO All the update views

    # --- General purpose URLs ---
    url(r'^$', views.welcome, name="welcome"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    # --- Node-related URLs ---
    url(r'^nodes/list/',
        ListView.as_view(
            model=Node,
            context_object_name='object_list',
            template_name="list_nodes.html"
        ), name='list_nodes'),

    url(r'^nodes/create/',
        CreateView.as_view(
            model=Node,
            context_object_name='form',
            fields='__all__',
            template_name='add_node.html',
            success_url=reverse_lazy('list_nodes'),
        ), name='add_node'),

    url(r'^nodes/delete/(?P<pk>[\d]+)/$',
        DeleteView.as_view(
            model=Node,
            context_object_name='node',
            template_name='delete_node.html',
            success_url=reverse_lazy('list_nodes'),
        ), name='delete_node'),

    # --- Producer-related URLs ---
    url(r'^producers/list/',
        ListView.as_view(
            model=Producer,
            context_object_name='object_list',
            template_name="list_producers.html"
        ), name='list_producers'),

    url(r'^producers/create/',
        CreateView.as_view(
            model=Producer,
            context_object_name='form',
            fields='__all__',
            template_name='add_producer.html',
            success_url=reverse_lazy('list_producers'),
        ), name='add_producer'),

    url(r'^producers/delete/(?P<pk>[\d]+)/$',
        DeleteView.as_view(
            model=Producer,
            context_object_name='producer',
            template_name='delete_producer.html',
            success_url=reverse_lazy('list_producers'),
        ), name='delete_producer'),

    # --- FPGA Model-related URLs ---
    url(r'^fpga_models/list/',
        ListView.as_view(
            model=FpgaModel,
            context_object_name='object_list',
            template_name="list_fpga_models.html"
        ), name='list_fpga_models'),

    url(r'^fpga_models/create/',
        CreateView.as_view(
            model=FpgaModel,
            context_object_name='form',
            fields='__all__',
            template_name='add_fpga_model.html',
            success_url=reverse_lazy('list_fpga_models'),
        ), name='add_fpga_model'),

    url(r'^fpga_models/delete/(?P<pk>[\d]+)/$',
        DeleteView.as_view(
            model=FpgaModel,
            context_object_name='fpga_model',
            template_name='delete_fpga_model.html',
            success_url=reverse_lazy('list_fpga_models'),
        ), name='delete_fpga_model'),

    # --- FPGA related URLs ---

    url(r'^fpgas/list/',
        ListView.as_view(
            model=Fpga,
            context_object_name='object_list',
            template_name="list_fpgas.html"
        ), name='list_fpgas'),

    url(r'^fpgas/create/',
        views.add_fpga,
        name='add_fpga'),

    url(r'^fpgas/delete/(?P<pk>[\d]+)/$',
        DeleteView.as_view(
            model=Fpga,
            context_object_name='fpga',
            template_name='delete_fpga.html',
            success_url=reverse_lazy('list_fpgas'),
        ), name='delete_fpga'),

    url(r'^fpgas/view/(?P<pk>[\d]+)/$',
        views.show_fpga,
        name='view_fpga'),

    # --- Region Type related URLs ---

    url(r'^region_types/create/',
        CreateView.as_view(
            model=RegionType,
            context_object_name='form',
            fields='__all__',
            template_name='add_region_type.html',
            success_url=reverse_lazy('list_region_types'),
        ), name='add_region_type'),

    url(r'^region_types/list/',
        ListView.as_view(
            model=RegionType,
            context_object_name='object_list',
            template_name="list_region_types.html"
        ), name='list_region_types'),

    url(r'^region_types/delete/(?P<pk>[\d]+)/$',
        DeleteView.as_view(
            model=RegionType,
            context_object_name='region_type',
            template_name='delete_region_type.html',
            success_url=reverse_lazy('list_region_types'),
        ), name='delete_region_type'),
]
