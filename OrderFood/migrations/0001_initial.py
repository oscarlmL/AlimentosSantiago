# Generated by Django 3.2.9 on 2021-11-30 15:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('rut_adm', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre_adm', models.CharField(max_length=50)),
                ('apat_adm', models.CharField(max_length=50)),
                ('amat_adm', models.CharField(max_length=50)),
                ('email_admin', models.CharField(max_length=50)),
                ('fono_admin', models.IntegerField()),
                ('contraseña1', models.CharField(max_length=100)),
                ('contraseña2', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'administrador',
            },
        ),
        migrations.CreateModel(
            name='Cajero',
            fields=[
                ('id_cajero', models.AutoField(primary_key=True, serialize=False)),
                ('nom_cajero', models.CharField(max_length=50)),
                ('email_cajero', models.CharField(max_length=50)),
                ('contraseña1', models.CharField(max_length=100)),
                ('contraseña2', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'cajero',
            },
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idplato', models.IntegerField()),
                ('cantidad', models.IntegerField()),
            ],
            options={
                'db_table': 'carrito',
            },
        ),
        migrations.CreateModel(
            name='categoriaPlato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'categoria_plato',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cli', models.CharField(max_length=50)),
                ('apaterno_cli', models.CharField(max_length=50)),
                ('amaterno_cli', models.CharField(max_length=50)),
                ('fono_cli', models.IntegerField()),
                ('email_cli', models.CharField(max_length=50)),
                ('saldo_cli', models.IntegerField(default=0, null=True)),
                ('contraseña1', models.CharField(max_length=100)),
                ('contraseña2', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Convenio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_emp', models.CharField(max_length=50)),
                ('saldo_cli', models.IntegerField(default=0, null=True)),
            ],
            options={
                'db_table': 'convenio',
            },
        ),
        migrations.CreateModel(
            name='EncCocina',
            fields=[
                ('id_enc_coc', models.AutoField(primary_key=True, serialize=False)),
                ('nom_enc_coc', models.CharField(max_length=100)),
                ('titulo', models.CharField(max_length=100)),
                ('exp_laboral', models.IntegerField()),
                ('email_enc_coc', models.EmailField(max_length=254)),
                ('celular', models.IntegerField()),
                ('contraseña1', models.CharField(max_length=100)),
                ('contraseña2', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'enc_cocina',
            },
        ),
        migrations.CreateModel(
            name='EncConvenio',
            fields=[
                ('id_enc_conv', models.AutoField(primary_key=True, serialize=False)),
                ('rut_enc_conv', models.CharField(max_length=100)),
                ('nom_enc_conv', models.CharField(max_length=100)),
                ('ap_enc_conv', models.CharField(max_length=100)),
                ('email_enc_conv', models.EmailField(max_length=254)),
                ('celular', models.IntegerField()),
                ('contraseña1', models.CharField(max_length=100)),
                ('contraseña2', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'enc_convenio',
            },
        ),
        migrations.CreateModel(
            name='Informes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_pedido', models.IntegerField()),
                ('id_plato', models.IntegerField()),
                ('fec_pedido', models.CharField(max_length=50)),
                ('total_pedido', models.IntegerField()),
                ('nom_plato', models.CharField(max_length=50)),
                ('nom_ing', models.CharField(max_length=50)),
                ('valor_ing', models.IntegerField()),
            ],
            options={
                'db_table': 'informes',
            },
        ),
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id_ing', models.AutoField(primary_key=True, serialize=False)),
                ('nom_ing', models.CharField(max_length=50)),
                ('descp_ing', models.CharField(max_length=50)),
                ('tipo_ing', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'ingrediente',
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_pago', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'pago',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nom_proveedor', models.CharField(max_length=50)),
                ('rol_local', models.CharField(max_length=50)),
                ('celular', models.IntegerField()),
                ('descripcion', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'proveedor',
            },
        ),
        migrations.CreateModel(
            name='Repartidor',
            fields=[
                ('id_repartidor', models.AutoField(primary_key=True, serialize=False)),
                ('rut_repartidor', models.CharField(max_length=50)),
                ('nombre_repartidor', models.CharField(max_length=50)),
                ('apellido_repartidor', models.CharField(max_length=50)),
                ('email_repartidor', models.CharField(max_length=50)),
                ('tipo_veh', models.CharField(max_length=50)),
                ('patente_veh', models.CharField(max_length=50)),
                ('celular', models.IntegerField(null=True)),
                ('contraseña1', models.CharField(max_length=100)),
                ('contraseña2', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'repartidor',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id_restaurante', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_rest', models.CharField(max_length=50)),
                ('direccion_rest', models.CharField(max_length=50)),
                ('imagen', models.ImageField(default=None, upload_to='restaurantes')),
            ],
            options={
                'db_table': 'restaurant',
            },
        ),
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id_suscrip', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_suscrip', models.CharField(max_length=50)),
                ('desc_suscrip', models.CharField(max_length=50)),
                ('administrador_rut_adm', models.ForeignKey(db_column='administrador_rut_adm', on_delete=django.db.models.deletion.DO_NOTHING, to='OrderFood.administrador')),
                ('enc_convenio_id_enc_conv', models.ForeignKey(db_column='enc_convenio_id_enc_conv', on_delete=django.db.models.deletion.DO_NOTHING, to='OrderFood.encconvenio')),
            ],
            options={
                'db_table': 'suscripción',
            },
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id_plato', models.AutoField(primary_key=True, serialize=False)),
                ('nom_plato', models.CharField(max_length=50)),
                ('valor_plato', models.IntegerField()),
                ('descripcion', models.CharField(max_length=50)),
                ('Imagen', models.ImageField(default=None, upload_to='platos')),
                ('Ingrediente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OrderFood.ingrediente')),
                ('Restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='OrderFood.restaurant')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrderFood.categoriaplato')),
            ],
            options={
                'db_table': 'plato',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(default=1)),
                ('precio', models.IntegerField()),
                ('horario_entrega', models.DateTimeField()),
                ('direccion', models.CharField(blank=True, default='', max_length=100)),
                ('tipo_entrega', models.CharField(choices=[['Delivery', 'Delivery'], ['Retiro en local', 'Retiro en local']], max_length=50)),
                ('celular', models.CharField(blank=True, default='', max_length=10)),
                ('fecha_pedido', models.DateField(default=datetime.datetime.today)),
                ('estado', models.CharField(choices=[['Pendiente', 'Pendiente'], ['Confirmado', 'Confirmado'], ['En ruta', 'En ruta'], ['Entregado', 'Entregado']], default='Pendiente', max_length=50)),
                ('cliente_id', models.ForeignKey(db_column='cliente_id', on_delete=django.db.models.deletion.CASCADE, to='OrderFood.cliente')),
                ('plato_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrderFood.plato')),
                ('restaurant_id_restaurante', models.ForeignKey(db_column='restaurant_id_restaurante', on_delete=django.db.models.deletion.DO_NOTHING, to='OrderFood.restaurant')),
                ('tipo_pago', models.ForeignKey(db_column='tipo_pago', on_delete=django.db.models.deletion.CASCADE, to='OrderFood.pago')),
            ],
            options={
                'db_table': 'pedido',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('rut_emp', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nom_emp', models.CharField(max_length=50)),
                ('nom_gerente', models.CharField(max_length=50)),
                ('cant_trabajadores', models.IntegerField()),
                ('enc_convenio_id_enc_conv', models.ForeignKey(db_column='enc_convenio_id_enc_conv', on_delete=django.db.models.deletion.DO_NOTHING, to='OrderFood.encconvenio')),
            ],
            options={
                'db_table': 'empresa',
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='empresa_rut_empresa',
            field=models.ForeignKey(db_column='empresa_rut_empresa', null=True, on_delete=django.db.models.deletion.CASCADE, to='OrderFood.empresa'),
        ),
        migrations.AddField(
            model_name='administrador',
            name='restaurant_id_restaurante',
            field=models.ForeignKey(db_column='restaurant_id_restaurante', default=1, on_delete=django.db.models.deletion.CASCADE, to='OrderFood.restaurant'),
        ),
        migrations.CreateModel(
            name='DetalleInsumos',
            fields=[
                ('id_det_ins', models.IntegerField(primary_key=True, serialize=False)),
                ('desc_det_ins', models.CharField(max_length=50)),
                ('valor_ing', models.IntegerField()),
                ('ingrediente_id_ing', models.ForeignKey(db_column='ingrediente_id_ing', on_delete=django.db.models.deletion.DO_NOTHING, to='OrderFood.ingrediente')),
                ('proveedor_id_proveedor', models.ForeignKey(db_column='proveedor_id_proveedor', on_delete=django.db.models.deletion.DO_NOTHING, to='OrderFood.proveedor')),
            ],
            options={
                'db_table': 'detalle_insumos',
                'unique_together': {('id_det_ins', 'ingrediente_id_ing', 'proveedor_id_proveedor')},
            },
        ),
        migrations.CreateModel(
            name='DetPago',
            fields=[
                ('precio_unidad', models.IntegerField()),
                ('total', models.IntegerField()),
                ('direccion_entrega', models.CharField(max_length=50)),
                ('pago_id_pago', models.ForeignKey(db_column='pago_id_pago', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='OrderFood.pago')),
                ('pedido_id_pedido', models.ForeignKey(db_column='pedido_id_pedido', on_delete=django.db.models.deletion.DO_NOTHING, to='OrderFood.pedido')),
                ('repartidor_id_repartidor', models.ForeignKey(db_column='repartidor_id_repartidor', on_delete=django.db.models.deletion.DO_NOTHING, to='OrderFood.repartidor')),
            ],
            options={
                'db_table': 'det_pago',
                'unique_together': {('pago_id_pago', 'pedido_id_pedido')},
            },
        ),
    ]
