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


User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/charts.html', {"customers": 10})



def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
        default_items = [qs_count, 23, 2, 3, 12, 2]
        data = {
                "labels": labels,
                "default": default_items,
        }
        print ("The data is",data)
        return Response(data)


def index(request):
    return render(request, 'public/home.html')

def reportes(request):
    return render(request, 'public/reportes.html')

def receipt(request):
    purchase = Purchase.objects.latest('date')
    pizzas = Pizza.objects.filter(purchase=purchase.pk)
    return render_to_response('public/receipt.html', {'purchase': purchase,'pizzas':pizzas})

def purchase_list_client(request):
    purchase = Purchase.objects.order_by('client_id')
    return render_to_response('public/purchase_list_client.html', {'purchase': purchase})

def purchase_list_ingredients(request):
    dict = {}
    ingredients = Ingredient.objects.all()

    for ingredient in ingredients:
         result =None
         with connection.cursor() as cursor:
            cursor.execute("""SELECT a.* from pizzeria_purchase as a, pizzeria_pizza as b
                            WHERE a.id = b.purchase_id AND b.id in (SELECT b.id from pizzeria_pizza as b, pizzeria_pizza_ingredient as c
                                            WHERE b.id = c.pizza_id and c.ingredient_id = %s)""",[ingredient.pk])
            result = cursor.fetchall()
         dict[ingredient.name] = result

    return render_to_response('public/purchase_list_ingredients.html', {'dict':dict})

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

class Pdf(View):

    def get(self, request):
        purchase = Purchase.objects.latest('date')
        pizzas = Pizza.objects.filter(purchase=purchase.pk)
        params = {
            'purchase': purchase,
            'pizzas': pizzas,
        }
        return Render.render('public/pdf.html', params)

class PurchaseList(ListView):
	model = Purchase
	template_name = 'public/purchase_list.html'

class PurchasePizzaCreate(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'public/purchase_form.html'
    success_url = reverse_lazy('receipt')

    def get_context_data(self, **kwargs):
        data = super(PurchasePizzaCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pizzas'] = PizzaFormSet(self.request.POST)
        else:
            data['pizzas'] = PizzaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pizzas = context['pizzas']
        with transaction.atomic():
            self.object = form.save()

            if pizzas.is_valid():
                pizzas.instance = self.object
                pizzas.save()

            self.object.calculate_price()
        return super(PurchasePizzaCreate, self).form_valid(form)
