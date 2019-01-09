from django.test import TestCase
from .models import Drink,Ingredient,Size
# Create your tests here.
""" Clase que contiene las pruebas al modelo de bebida"""
class DrinkModelTests(TestCase):

    """ El precio de una bebida debe ser positivo"""
    def test_drink_price_must_be_positive(self):
        #Crear Bebida
        drink = Drink(name='Bebida Prueba',price=4)
        #Comprobar las validaciones
        self.assertTrue(drink.clean())

""" Clase que contiene las pruebas al modelo de ingrediente"""
class IngredientModelTests(TestCase):

    """ El precio de un ingrediente debe ser positivo"""
    def test_ingredient_price_must_be_positive(self):
        #Crear Bebida
        ingredeint = Ingredient(name='Ingrediente Prueba',price=4)
        #Comprobar las validaciones
        self.assertTrue(ingredient.clean())
