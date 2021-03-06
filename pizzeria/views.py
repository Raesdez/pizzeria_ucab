from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.views.generic import View, CreateView, ListView
from pizzeria.models import Purchase, Pizza, Ingredient, Size
from pizzeria.forms import PizzaForm, PurchaseForm, PizzaFormSet
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction, connection
from pizzeria.render import Render

""" Resumen: carga la template que tiene el menu de los reportes"""
def index(request):
    return render(request, 'public/home.html')

""" Resumen: carga la template que tiene el menu de los reportes"""
def reportes(request):
    return render(request, 'public/reportes.html')

""" Resumen: obtiene la informacion de la compra y de las pizzas y renderiza el
             template de recibo"""
def receipt(request):
    purchase = Purchase.objects.latest('date')
    pizzas = Pizza.objects.filter(purchase=purchase.pk)
    return render_to_response('public/receipt.html', {'purchase': purchase,'pizzas':pizzas})

""" Carga la template del reporte de compras por cliente y envia la lista de compras ordenadas por cliente
    que luego seran agrupadas"""
def purchase_list_client(request):
    purchase = Purchase.objects.order_by('client_id')
    return render_to_response('public/purchase_list_client.html', {'purchase': purchase})

""" Similar al reporte de cliente, carga el template enviando las compras ordenadas por fecha"""
def purchase_list_date(request):
    purchase = Purchase.objects.order_by('date')
    return render_to_response('public/purchase_list_date.html', {'purchase': purchase})

""" Este metodo utiliza un query raw para poder hacer un join completo y Obtener
    las compras con al menos una pizza con el ingrediente correspondiente"""
def purchase_list_ingredients(request):
    dict = {} #El diccionario tendra los ingredientes como clave y las compras como valores
    ingredients = Ingredient.objects.all()
    #Iterar todos los ingredeintes
    for ingredient in ingredients:
         result =None
         with connection.cursor() as cursor:
            cursor.execute("""SELECT a.* from pizzeria_purchase as a, pizzeria_pizza as b
                            WHERE a.id = b.purchase_id AND b.id in (SELECT b.id from pizzeria_pizza as b, pizzeria_pizza_ingredient as c
                                            WHERE b.id = c.pizza_id and c.ingredient_id = %s)""",[ingredient.pk])
            result = cursor.fetchall() #Obtener resultados de los queries
         dict[ingredient.name] = result

    return render_to_response('public/purchase_list_ingredients.html', {'dict':dict})

""" Similar al metodo del reporte de ingredientes, realiza un query raw para hacer un join
    y obtener las ventas con al menos una pizza que tenga el tamano indicado"""
def purchase_list_sizes(request):
    dict = {}
    sizes = Size.objects.all()

    for size in sizes:
         result =None
         with connection.cursor() as cursor:
            cursor.execute("""SELECT a.* from pizzeria_purchase as a
                            WHERE a.id in (SELECT b.id from pizzeria_pizza as b
                                            WHERE b.size_id = %s)""",[size.pk])
            result = cursor.fetchall()
         dict[size.name] = result

    return render_to_response('public/purchase_list_sizes.html', {'dict':dict})

"""Resumen: View Class que contiene el metodo para enviar los datos de la compra
            al template que sera renderizado como PDF"""
class Pdf(View):

    def get(self, request):
        purchase = Purchase.objects.latest('date')
        pizzas = Pizza.objects.filter(purchase=purchase.pk)
        params = {
            'purchase': purchase,
            'pizzas': pizzas,
        }
        return Render.render('public/pdf.html', params)

""" Resumen: ListView que consulta todas las compras para ser cargadas en el template del reporte"""
class PurchaseList(ListView):
	model = Purchase
	template_name = 'public/purchase_list.html'

""" Resumen: Clase en forma de Create View que carga el form de Compra, luego almacena
             la compra y finalmente le asigna los datos de las pizzas en el form anidado """
class PurchasePizzaCreate(CreateView):
    model = Purchase
    form_class = PurchaseForm #Cargar el form
    template_name = 'public/purchase_form.html'
    success_url = reverse_lazy('receipt') #Ir al recibo posteriormente

    def get_context_data(self, **kwargs):
        data = super(PurchasePizzaCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pizzas'] = PizzaFormSet(self.request.POST)
        else:
            data['pizzas'] = PizzaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pizzas = context['pizzas'] #Obtener las pizzas del contexto
        with transaction.atomic():
            self.object = form.save()   #Almacenar la compra

            if pizzas.is_valid():
                pizzas.instance = self.object #Indicar la entidad padre de las pizzas
                pizzas.save()   #Alcacenar las pizzas

            self.object.calculate_price()
        return super(PurchasePizzaCreate, self).form_valid(form)
