from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Cliente, Proveedor, Plato, Repartidor,Pedido, Empresa


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
        fields = ['nombre_cli', 'apaterno_cli', 'amaterno_cli', 'fono_cli', 'email_cli', 'saldo_cli', 'pass_field', 'direccion_cliente', 'convenio']


    nombre_cli = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    apaterno_cli = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    amaterno_cli = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    fono_cli = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email_cli = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    saldo_cli = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    pass_field = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    direccion_cliente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    convenio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class GestionEmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ['rut_emp','nom_emp', 'nom_gerente', 'cant_trabajadores','enc_convenio_id_enc_conv']
        #fields = '__all__'

        rut_emp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','onkeyup':'formatoRut(this)'}))