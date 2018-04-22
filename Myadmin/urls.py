import importlib
from django.conf.urls import url
from Myadmin import views
urlpatterns = [
    url(r'^$', views.index,name="index"),
    url(r'^(?P<app_name>\w+)$', views.show_app,name="show_app"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)$', views.show_table,name="show_table"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/add/$', views.table_add,name="table_add"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<table_id>\d+)/change/$', views.table_edit,name="table_edit"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<table_id>\d+)/delete/$', views.table_delete,name="table_delete"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<table_id>\d+)/change/password$', views.password_reset,name="table_delete"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<table_id>\d+)/enrollment$', views.enrollment,name="enrollment"),
]
