from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, CreateView
from pizzeria.models import Purchase, Pizza
from pizzeria.forms import PizzaForm, PurchaseForm, PizzaFormSet
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction


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

class PurchasePizzaCreate(CreateView):
    model = Purchase
    fields = ['client_id','client_name','drink',]
    template_name = 'public/purchase_form.html'
    success_url = reverse_lazy('index')

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
        return super(PurchasePizzaCreate, self).form_valid(form)


class PizzaCreate(CreateView):
    model = Pizza
    template_name = 'public/pizza_form.html'
    form_class = PizzaForm
    second_form_class = PurchaseForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(PizzaCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
    	       context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
    	       context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            pizza = form.save(commit=False)
            pizza.purchase = form2.save()
            pizza = form.save()
            pizza.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
