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

from .views import index,PurchasePizzaCreate, receipt, PurchaseList, reportes, Pdf, purchase_list_client
from .views import purchase_list_ingredients, purchase_list_sizes, purchase_list_date

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^purchase', PurchasePizzaCreate.as_view(), name='compra'),
    #Rutas para los reportes
    url(r'^reportes$', reportes, name='reportes'),
    url(r'^reportes/lista_ventas$', PurchaseList.as_view(), name='lista_ventas'),
    url(r'^reportes/lista_ventas_client$', purchase_list_client, name='lista_ventas_client'),
    url(r'^reportes/lista_ventas_ingredientes$',purchase_list_ingredients,name='lista_ventas_ingredientes'),
    url(r'^reportes/lista_ventas_tamanos$',purchase_list_sizes,name='lista_ventas_tamanos'),
    url(r'^reportes/lista_ventas_dia$',purchase_list_date,name='lista_ventas_dia'),
    #Ruta para el recibo y Path para la factura en PDF
    url(r'^receipt',receipt,name='receipt'),
    path('render/pdf/', Pdf.as_view(), name='Pdf'),
]
