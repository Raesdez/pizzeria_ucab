from django.test import TestCase
from .models import Drink,Ingredient,Size
# Create your tests here.
class DrinkModelTests(TestCase):

    def test_drink_price_must_be_positive(self):
        #Crear Bebida
        drink = Drink(name='Bebida Prueba',price=4)
        #Comprobar las validaciones
        self.assertTrue(drink.clean())

class IngredientModelTests(TestCase):

    def test_ingredient_price_must_be_positive(self):
        #Crear Bebida
        ingredeint = Ingredient(name='Ingrediente Prueba',price=4)
        #Comprobar las validaciones
        self.assertTrue(ingredient.clean())
