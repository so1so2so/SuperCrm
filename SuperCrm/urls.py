"""SuperCrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import views
import jet
urlpatterns = [
    url(r'^$', views.Mylogin,name="login"),
    url(r'^logout$', views.Mylogout,name="logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^crm/', include("crm.urls")),
    url(r'^students/', include("students.urls")),
    url(r'^Myadmin/', include("Myadmin.urls")),
    # url(r'^jet/', include('jet.urls', 'jet')),
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
]
