# Generated by Django 2.1.5 on 2019-01-09 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0009_remove_pizza_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]