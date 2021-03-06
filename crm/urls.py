
from django.conf.urls import url
from crm import views
urlpatterns = [
    url(r'^index/', views.index,name="index"),
    url(r'^$', views.crm,name="crm"),
    url(r'^teacher/', views.teacher,name="teacher"),
    url(r'^sale/', views.sale,name="sale"),
    url(r'^customer/', views.customer,name="customer"),
    url(r'^payment/(?P<enroll_id>\d+)', views.payment,name="payment"),
]
