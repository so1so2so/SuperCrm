
from django.conf.urls import url
from Myadmin import views
urlpatterns = [
    url(r'^$', views.index,name="index"),
]
