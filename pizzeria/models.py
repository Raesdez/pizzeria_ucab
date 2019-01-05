from django.db import models

# Create your models here.

class Size(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.FloatField(default=0, blank=False)

    def __str__(self):
        return '{} {}'.format(self.name, self.price)

class Ingredient(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.FloatField(default=0, blank=False)

    def __str__(self):
        return '{} {}'.format(self.name, self.price)

class Drink(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.FloatField(default=0, blank=False)
    size = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return '{} {} {}'.format(self.name, self.size, self.price)

class Purchase(models.Model):
    total_price = models.FloatField(default=0, blank=False)
    date = models.DateField(blank=True, null=True)
    client_id = models.IntegerField(default=0, blank=False)
    client_name = models.CharField(max_length=50, blank=False)
    drink = models.ManyToManyField(Drink, blank=True, null=True)

class Pizza(models.Model):
    purchase = models.ForeignKey(Purchase, blank=False, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, blank=False, on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient)
