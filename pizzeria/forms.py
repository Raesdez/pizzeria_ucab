from django import forms
from django.forms import inlineformset_factory #Para poder anidar modelos
from pizzeria.models import Purchase, Pizza

""" Resumen: clase que contiene el formulario para crear una pizza """
class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza #Modelo
        #Campos
        fields = [
            'size',
            'ingredient'
        ]
        #Etiquetas con el nombre que el usuario vera
        labels = {
            'size': 'Tamaño',
            'ingredient': 'Ingredientes',
        }
        #La forma se input para cada campo
        widgets = {
            'size': forms.RadioSelect(),
            'ingredient': forms.CheckboxSelectMultiple(),
        }

""" Importante: aqui se indica que las pizzas estan anidadas a las compras"""
PizzaFormSet = inlineformset_factory(Purchase, Pizza,
                                            form=PizzaForm, extra=1)

""" Resumen : clase que contiene el formulario de una compra"""
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase #Modelo
        #Campos
        fields = [
            'client_id',
            'client_name',
            'drink',
        ]
        #Etiquetas con el nombre que el usuario vera
        labels = {
            'client_id': 'Cédula',
            'client_name': 'Nombre',
            'drink': 'Bebidas',
        }
        #La forma se input para cada campo
        widgets = {
            'client_id': forms.TextInput(),
            'client_name': forms.TextInput(),
            'drink': forms.CheckboxSelectMultiple(),
        }
