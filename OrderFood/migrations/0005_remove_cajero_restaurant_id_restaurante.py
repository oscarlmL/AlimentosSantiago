# Generated by Django 3.2.7 on 2021-11-11 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderFood', '0004_auto_20211111_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cajero',
            name='restaurant_id_restaurante',
        ),
    ]
