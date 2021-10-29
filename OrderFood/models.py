from django.db import models
from django.utils.translation import TranslatorCommentWarning


class Administrador(models.Model):
    # This field type is a guess.
    rut_adm = models.CharField(max_length=50, primary_key=True)
    # Field renamed because it was a Python reserved word. This field type is a guess.
    nombre_adm = models.CharField(max_length=50)  # This field type is a guess.
    apat_adm = models.CharField(max_length=50)  # This field type is a guess.
    amat_adm = models.CharField(max_length=50)  # This field type is a guess.
    # This field type is a guess.
    email_admin = models.CharField(max_length=50)
    fono_admin = models.IntegerField()
    contraseña1 = models.CharField(max_length=100)
    contraseña2 = models.CharField(max_length=100)
    restaurant_id_restaurante = models.ForeignKey(
        'Restaurant', models.CASCADE, db_column='restaurant_id_restaurante' ,default=1)
    class Meta:
        db_table = 'administrador'
    
    def cuentaAdmin(self):
        self.save()

    @staticmethod
    def get_admin_by_email(email_admin):
        try:
            return Administrador.objects.get(email_admin=email_admin)
        except:
            return False



class Cajero(models.Model):
    id_cajero = models.AutoField(primary_key=True)
    nom_cajero = models.CharField(max_length=50)  # This field type is a guess.
    restaurant_id_restaurante = models.ForeignKey(
        'Restaurant', models.DO_NOTHING, db_column='restaurant_id_restaurante')

    class Meta:
        db_table = 'cajero'


class Cliente(models.Model):
    # This field type is a guess.
    rut_cli = models.CharField(max_length=50, primary_key=True)
    nombre_cli = models.CharField(db_column='nombre_cli',max_length=50)  # This field type is a guess.
    apaterno_cli = models.CharField(max_length=50)
    amaterno_cli = models.CharField(max_length=50)
    fono_cli = models.IntegerField()
    email_cli = models.CharField(max_length=50)  # This field type is a guess.
    saldo_cli = models.IntegerField()
    # Field renamed because it was a Python reserved word. This field type is a guess.
    password = models.TextField(db_column='password')
    # This field type is a guess.
    # Domicilio = models.CharField(max_length=50)
    Domicilio = models.TextField(db_column='direccion_cliente', null=True)
    convenio = models.CharField(max_length=1)

    class Meta:
        db_table = 'cliente'

class Convenio(models.Model):
    rut_cli = models.CharField(max_length=50)  # This field type is a guess.
    nom_cli = models.CharField(max_length=50)  # This field type is a guess.
    nom_emp = models.CharField(max_length=50)  # This field type is a guess.
    rut_emp = models.CharField(max_length=50)  # This field type is a guess.
    # This field type is a guess.
    tipo_suscrip = models.CharField(max_length=50)

    class Meta:
        db_table = 'convenio'


class DetPago(models.Model):
    precio_unidad = models.IntegerField()
    total = models.IntegerField()
    # This field type is a guess.
    direccion_entrega = models.CharField(max_length=50)
    pago_id_pago = models.ForeignKey(
        'Pago', models.DO_NOTHING, db_column='pago_id_pago', primary_key=True)
    pedido_id_pedido = models.ForeignKey(
        'Pedido', models.DO_NOTHING, db_column='pedido_id_pedido')
    repartidor_id_repartidor = models.ForeignKey(
        'Repartidor', models.DO_NOTHING, db_column='repartidor_id_repartidor')

    class Meta:
        db_table = 'det_pago'
        unique_together = (('pago_id_pago', 'pedido_id_pedido'),)


class DetalleInsumos(models.Model):
    id_det_ins = models.IntegerField(primary_key=True)
    # This field type is a guess.
    desc_det_ins = models.CharField(max_length=50)
    valor_ing = models.IntegerField()
    ingrediente_id_ing = models.ForeignKey(
        'Ingrediente', models.DO_NOTHING, db_column='ingrediente_id_ing')
    proveedor_id_proveedor = models.ForeignKey(
        'Proveedor', models.DO_NOTHING, db_column='proveedor_id_proveedor')

    class Meta:
        db_table = 'detalle_insumos'
        unique_together = (
            ('id_det_ins', 'ingrediente_id_ing', 'proveedor_id_proveedor'),)


class Empresa(models.Model):
    # This field type is a guess.
    rut_emp = models.CharField(max_length=50, primary_key=True)
    nom_emp = models.CharField(max_length=50)  # This field type is a guess.
    # This field type is a guess.
    nom_gerente = models.CharField(max_length=50)
    cant_trabajadores = models.IntegerField()
    enc_convenio_id_enc_conv = models.ForeignKey(
        'EncConvenio', models.DO_NOTHING, db_column='enc_convenio_id_enc_conv')

    class Meta:
        db_table = 'empresa'


class EncCocina(models.Model):
    id_enc_coc = models.AutoField(primary_key=True)
    # This field type is a guess.
    nom_enc_coc = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)  # This field type is a guess.
    exp_laboral = models.IntegerField()
    email_enc_coc = models.EmailField()  # This field type is a guess.
    celular = models.IntegerField()
    contraseña1 = models.CharField(max_length=100)
    contraseña2 = models.CharField(max_length=100)

    def cuentaEncargadoCocina(self):
        self.save()

    def siExiste(self):
        if EncCocina.objects.filter(email_enc_coc=self.email_enc_coc):
            return True
        return False

    @staticmethod
    def get_enc_cocina_by_email(email_enc_coc):
        try:
            return EncCocina.objects.get(email_enc_coc=email_enc_coc)
        except:
            return False


    class Meta:
        db_table = 'enc_cocina'


class EncConvenio(models.Model):
    id_enc_conv = models.AutoField(primary_key=True)
    # This field type is a guess.
    rut_enc_conv = models.CharField(max_length=100)
    # This field type is a guess.
    nom_enc_conv = models.CharField(max_length=100)
    # This field type is a guess.
    ap_enc_conv = models.CharField(max_length=100)
    email_enc_conv = models.EmailField()  # This field type is a guess.
    celular = models.IntegerField()
    contraseña1 = models.CharField(max_length=100)
    contraseña2 = models.CharField(max_length=100)

    def cuentaEncargadoConvenio(self):
        self.save()

    def emailExiste(self):
        if EncConvenio.objects.filter(email_enc_conv=self.email_enc_conv):
            return True
        return False
    
    @staticmethod
    def get_enc_convenio_by_email(email_enc_conv):
        try:
            return EncConvenio.objects.get(email_enc_conv=email_enc_conv)
        except:
            return False


    def rutExiste(self):
        if EncConvenio.objects.filter(rut_enc_conv=self.rut_enc_conv):
            return True
        return False

    class Meta:
        db_table = 'enc_convenio'


class Informes(models.Model):
    id_pedido = models.IntegerField()
    id_plato = models.IntegerField()
    fec_pedido = models.CharField(max_length=50)  # This field type is a guess.
    total_pedido = models.IntegerField()
    nom_plato = models.CharField(max_length=50)  # This field type is a guess.
    nom_ing = models.CharField(max_length=50)  # This field type is a guess.
    valor_ing = models.IntegerField()

    class Meta:
        db_table = 'informes'


class Ingrediente(models.Model):
    id_ing = models.AutoField(primary_key=True)
    nom_ing = models.CharField(max_length=50)  # This field type is a guess.
    descp_ing = models.CharField(max_length=50)   # This field type is a guess.
    tipo_ing = models.CharField(max_length=50)  # This field type is a guess.

    class Meta:
        db_table = 'ingrediente'


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    tipo_pago = models.CharField(max_length=50)  # This field type is a guess.

    class Meta:
        db_table = 'pago'


#OPCIONES ESTADO PEDIDO
estado_pedido = [
    ['Pendiente', "Pendiente"],
    ['Confirmado', "Confirmado"],
    ['En ruta', "En ruta"],
    ['Entregado', "Entregado"]

]

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, choices=estado_pedido)   # This field type is a guess.
    # This field type is a guess.
    fecha_pedido = models.CharField(max_length=50)
    cliente_rut_cli = models.ForeignKey(
        Cliente, models.DO_NOTHING, db_column='cliente_rut_cli')
    restaurant_id_restaurante = models.ForeignKey(
        'Restaurant', models.DO_NOTHING, db_column='restaurant_id_restaurante')

    class Meta:
        db_table = 'pedido'


class Plato(models.Model):
    id_plato = models.AutoField(primary_key=True)
    nom_plato = models.CharField(max_length=50)   # This field type is a guess.
    valor_plato = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    Ingrediente = models.ForeignKey('Ingrediente', on_delete=models.PROTECT, null=True)
    Restaurant = models.ForeignKey('Restaurant', on_delete=models.PROTECT, null=True)
    Imagen = models.ImageField(default = None, upload_to="platos")

    @staticmethod
    def get_all_platos():
        return Plato.objects.all()

    class Meta:
        db_table = 'plato'


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    rol_local = models.CharField(max_length=50)  # This field type is a guess.
    # This field type is a guess.models.CharField(max_length=50)
    nom_proveedor = models.CharField(max_length=50)
    celular = models.IntegerField()
    descripcion = models.CharField(max_length=100)

    class Meta:
        db_table = 'proveedor'

    def __str__(self): 
        return self.nom_proveedor

        

class Repartidor(models.Model):
    id_repartidor = models.AutoField(primary_key=True)
    rut_repartidor = models.CharField(max_length=50)
    # This field type is a guess.
    nombre_repartidor = models.CharField(max_length=50)
    # This field type is a guess.
    apellido_repartidor = models.CharField(max_length=50)
    email_repartidor = models.CharField(max_length=50)
    # This field type is a guess.
    tipo_veh = models.CharField(max_length=50)
    patente_veh = models.CharField(max_length=50)
    celular = models.IntegerField(null=True)
    contraseña1 = models.CharField(max_length=100)
    contraseña2 = models.CharField(max_length=100)

    def cuentaRepartidor(self):
        self.save()

    def emailExiste(self):
        if Repartidor.objects.filter(email_repartidor=self.email_repartidor):
            return True
        return False

    def rutExiste(self):
        if Repartidor.objects.filter(rut_repartidor=self.rut_repartidor):
            return True
        return False

    def patenteExiste(self):
        if Repartidor.objects.filter(patente_veh=self.patente_veh):
            return True
        return False

    @staticmethod
    def get_repartidor_by_email(email_repartidor):
        try:
            return Repartidor.objects.get(email_repartidor=email_repartidor)
        except:
            return False



    class Meta:
        db_table = 'repartidor'


class Restaurant(models.Model):
    id_restaurante = models.AutoField(primary_key=True)
    # This field type is a guess.
    nombre_rest = models.CharField(max_length=50)
    # This field type is a guess.
    direccion_rest = models.CharField(max_length=50)
    # This field type is a guess.
    comuna_rest = models.CharField(max_length=50)

    class Meta:
        db_table = 'restaurant'


class Suscripcion(models.Model):
    id_suscrip = models.AutoField(primary_key=True)
    # This field type is a guess.
    tipo_suscrip = models.CharField(max_length=50)
    # This field type is a guess.
    desc_suscrip = models.CharField(max_length=50)
    administrador_rut_adm = models.ForeignKey(
        Administrador, models.DO_NOTHING, db_column='administrador_rut_adm')
    enc_convenio_id_enc_conv = models.ForeignKey(
        EncConvenio, models.DO_NOTHING, db_column='enc_convenio_id_enc_conv')

    class Meta:
        db_table = 'suscripción'
