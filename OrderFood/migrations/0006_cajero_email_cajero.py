# Generated by Django 3.2.7 on 2021-11-11 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderFood', '0005_remove_cajero_restaurant_id_restaurante'),
    ]

    operations = [
        migrations.AddField(
            model_name='cajero',
            name='email_cajero',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
