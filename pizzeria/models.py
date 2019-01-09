from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError


# Create your models here.

class Size(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.FloatField(default=0, blank=False)

    def __str__(self):
        return '{} {}'.format(self.name, self.price)

    def clean(self):
        if self.price<0:
            raise ValidationError('El precio debe ser positivo')
        else:
            return True

class Ingredient(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.FloatField(default=0, blank=False)

    def __str__(self):
        return '{} {}'.format(self.name, self.price)

    def clean(self):
        if self.price<0:
            raise ValidationError('El precio debe ser positivo')
        else:
            return True

class Drink(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.FloatField(default=0, blank=False)
    size = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return '{} {} {}'.format(self.name, self.size, self.price)

    def clean(self):
        if self.price<0:
            raise ValidationError('El precio debe ser positivo')
        else:
            return True

class Purchase(models.Model):
    total_price = models.FloatField(default=0, blank=False)
    date = models.DateField(auto_now_add=True)
    client_id = models.IntegerField(default=0, blank=False)
    client_name = models.CharField(max_length=50, blank=False)
    drink = models.ManyToManyField(Drink, blank=True, null=True)

    """Resumen: metodo que es llamado para calcular el precio de una compra """
    def calculate_price(self):
        result = 0.00

        #Obtener lista de pizzas y sumar los ingredientes y el tamano de cada una
        pizzas_list = Pizza.objects.filter(purchase=self.pk)
        for pizza in pizzas_list:
            sum = (pizza.ingredient.all().aggregate(Sum('price')))['price__sum']
            result += (sum + pizza.size.price) if sum != None else pizza.size.price

        #Obtener la suma de las bebidas de la compra
        sum = self.drink.all().aggregate(Sum('price'))['price__sum']
        result += sum if sum != None else 0

        #Asignar y guardar cambios al pedido
        self.total_price = result
        self.save()

class Pizza(models.Model):
    purchase = models.ForeignKey(Purchase, blank=False, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, blank=False, on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient)
