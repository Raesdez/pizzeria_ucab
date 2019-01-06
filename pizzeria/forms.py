from django import forms
from django.forms import inlineformset_factory
from pizzeria.models import Purchase, Pizza

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = [
            'size',
            'ingredient'
        ]
        labels = {
            'size': 'Tamaño',
            'ingredient': 'Ingredientes',
        }
        widgets = {
            'size': forms.RadioSelect(),
            'ingredient': forms.CheckboxSelectMultiple(),
        }

PizzaFormSet = inlineformset_factory(Purchase, Pizza,
                                            form=PizzaForm, extra=1)
"""
class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = [
            'size',
            'ingredient'
        ]
        labels = {
            'size': 'Tamaño',
            'ingredient': 'Ingredientes',
        }
        widgets = {
            'size': forms.RadioSelect(),
            'ingredient': forms.CheckboxSelectMultiple(),
        }
"""
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'client_id',
            'client_name',
            'drink',
        ]
        labels = {
            'client_id': 'Cédula',
            'client_name': 'Nombre',
            'drink': 'Bebidas',
        }
        widgets = {
            'client_id': forms.TextInput(),
            'client_name': forms.TextInput(),
            'drink': forms.CheckboxSelectMultiple(),
        }
