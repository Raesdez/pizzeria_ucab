from django.db import models

# Create your models here.

class Size(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.IntegerField(default=0, blank=False)
    quantity = models.IntegerField(default=0, blank=False)

class Ingredient(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.IntegerField(default=0, blank=False)
    quantity = models.IntegerField(default=0, blank=False)

class Drink(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.IntegerField(default=0, blank=False)
    quantity = models.IntegerField(default=0, blank=False)
    size = models.CharField(max_length=50, blank=False)

class Purchase(models.Model):
    total_price = models.IntegerField(default=0, blank=False)
    date = models.DateField()
    client_id = models.IntegerField(default=0, blank=False)
    client_name = models.CharField(max_length=50, blank=False)
    drink = models.ManyToManyField(Drink)

class Pizza(models.Model):
    purchase = models.ForeignKey(Purchase, blank=False, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, blank=False, on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient)
