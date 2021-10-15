from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Cliente, Proveedor, Plato, Repartidor,Pedido
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class ProveedorForm(forms.ModelForm):

    class Meta: 
        model = Proveedor
        fields = ['rol_local', 'nom_proveedor','celular','descripcion']

    rol_local = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nom_proveedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    celular = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


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
        fields = '__all__'
        
        

class RepartidorForm(forms.ModelForm):

    class Meta:
        model = Repartidor
        fields = ['rut_repartidor', 'nombre_repartidor','apellido_repartidor','email_repartidor','patente_veh', 'celular','contraseña1','contraseña2']
    


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['rut_cli','nombre_cli', 'apaterno_cli','amaterno_cli', 'fono_cli', 'email_cli', 'saldo_cli', 'password', 'Domicilio', 'convenio']


    # RUT = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # apaterno_cli = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    # amaterno_cli = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    # fono_cli = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # email_cli = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # saldo_cli = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    Domicilio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # convenio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))