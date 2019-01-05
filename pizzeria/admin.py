from django.contrib import admin

# Register your models here.
from .models import Size, Ingredient, Drink

admin.site.register(Size)
admin.site.register(Ingredient)
admin.site.register(Drink)
