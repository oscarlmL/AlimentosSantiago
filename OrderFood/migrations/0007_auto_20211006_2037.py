# Generated by Django 2.2.13 on 2021-10-06 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderFood', '0006_auto_20211005_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repartidor',
            name='celular',
            field=models.IntegerField(null=True),
        ),
    ]
