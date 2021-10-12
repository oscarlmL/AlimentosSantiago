from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Proveedor, Plato, Repartidor,Pedido


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
    
