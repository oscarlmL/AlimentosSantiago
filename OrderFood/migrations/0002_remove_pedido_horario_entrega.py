# Generated by Django 3.2.9 on 2021-11-09 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderFood', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='horario_entrega',
        ),
    ]
