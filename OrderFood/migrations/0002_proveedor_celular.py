# Generated by Django 2.2.13 on 2021-10-01 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderFood', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='celular',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
