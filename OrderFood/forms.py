from django import forms
import django
from django.db.models import fields
from django.forms import widgets
from .models import Cliente, Proveedor, Plato, Repartidor,Pedido, Empresa, Carrito
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class ProveedorForm(forms.ModelForm):

    # def clean_nom_proveedor(self):
    #nom_proveedor = self.cleaned_data["nom_proveedor"]
    #existe = Proveedor.objects.filter(nom_proveedor__iexact=nom_proveedor).exists()

    # if existe:
    #raise ValidationError("Este nombre ya existe")

    # return nom_proveedor

    class Meta:
        model = Proveedor
        fields = ['nom_proveedor','rol_local','celular','descripcion']

    class Meta:
        model = Proveedor
        fields = ['nom_proveedor', 'rol_local', 'celular', 'descripcion']
    nom_proveedor = forms.CharField(max_length=49,widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}), label='Nombre del Proveedor')
    rol_local = forms.CharField(max_length=49, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ej: comida china, japonesa, peruana, insumos'}), label='Rol del Local')
    celular = forms.CharField(min_length=9, max_length=9, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'tu celular ej: 977079248'}), label='Celular de Contacto')
    descripcion = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Tu oferta de productos, empresa, dirección'}), label='Descripción de la oferta a realizar')



        
class CarritoForm(forms.ModelForm):

    class Meta:
        model = Carrito
        fields = ['idplato', 'cantidad']

        fields = ['nom_proveedor', 'rol_local', 'celular', 'descripcion']
    nom_proveedor = forms.CharField(max_length=49,widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}), label='Nombre del Proveedor')
    rol_local = forms.CharField(max_length=49, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ej: comida china, japonesa, peruana, insumos'}), label='Rol del Local')
    celular = forms.CharField(min_length=9, max_length=9, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'tu celular ej: 977079248'}), label='Telefono/Celular de Contacto')
    descripcion = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Tu oferta de productos, empresa, dirección'}), label='Descripción de la oferta a realizar')


class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            "fecha_pedido": forms.SelectDateWidget()
        }


class PlatoForm(forms.ModelForm):

    class Meta:
        model = Plato
        fields = ['nom_plato', 
                'descripcion',
                 'valor_plato',
                # 'Ingrediente',
                # 'Restaurant',
                'Imagen'
                ]
        labels = {'nom_plato':'Nombre del Plato',
            'descripcion':'Descripción',
            'valor_plato': 'Valor del Plato',
            # 'Ingrediente':'Seleccionar Ingrediente',
            # 'Restaurant':'Seleccionar Restaurante',
            'Imagen':'Subir Imagen del Plato'

            
        }


class RepartidorForm(forms.ModelForm):

    class Meta:
        model = Repartidor
        fields = ['rut_repartidor', 'nombre_repartidor', 'apellido_repartidor',
                  'email_repartidor', 'patente_veh', 'celular', 'contraseña1', 'contraseña2']


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['rut_cli', 'nombre_cli', 'apaterno_cli', 'amaterno_cli', 'fono_cli',
                  'email_cli', 'saldo_cli', 'convenio', 'contraseña1', 'contraseña2']

    rut_cli = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Rut', 'label': ''}), label='')
    nombre_cli = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre'}), label='')
    apaterno_cli = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}), label='')
    amaterno_cli = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}), label='')
    fono_cli = forms.CharField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Teléfono'}), label='')
    email_cli = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}), label='')
    saldo_cli = forms.CharField(widget=forms.HiddenInput(), initial=0)
    convenio = forms.CharField(widget=forms.HiddenInput(), initial=0)
    contraseña1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña'}), label='')
    contraseña2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirme Contraseña'}), label='')


class GestionEmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ['rut_emp', 
                'nom_emp', 
                'nom_gerente',
                'cant_trabajadores', 
                'enc_convenio_id_enc_conv']
        labels = {'enc_convenio_id_enc_conv':'Encargado de Convenio'}

    #labels = {'rut_emp':'Run Empresa'}
    rut_emp = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'onkeyup': 'formatoRut(this)', 'placeholder': 'Run Empresa', 'display': None}), label='Run Empresa')
    nom_emp = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre Empresa'}), label='Nombre de la Empresa')
    nom_gerente = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre Gerente'}), label='Nombre del Gerente')
    cant_trabajadores = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Cantidad Trabajadores'}), label='Cantidad de Trabajadores')
    #rut_emp = forms.CharField(max_length=9)
