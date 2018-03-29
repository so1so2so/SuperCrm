
from django.conf.urls import url
from crm import views
urlpatterns = [
    url(r'^$', views.sale_index,name="sale"),
    url(r'^customer/', views.customer,name="customer"),
]
