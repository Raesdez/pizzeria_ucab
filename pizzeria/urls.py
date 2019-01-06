"""charts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from .views import HomeView, get_data, ChartData, index,PurchasePizzaCreate, receipt, PurchaseList, reportes


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^reportes$', reportes, name='reportes'),
    #url(r'^reportes', HomeView.as_view(), name='home'),
    #url(r'^api/data/$', get_data, name='api-data'),
    #url(r'^api/chart/data/$', ChartData.as_view()),
    url(r'^purchase', PurchasePizzaCreate.as_view(), name='compra'),
    url(r'^receipt',receipt,name='receipt'),
    url(r'^reportes/lista_ventas', PurchaseList.as_view(), name='lista_ventas'),
]
