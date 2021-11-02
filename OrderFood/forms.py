from django import forms
import django
from django.db.models import fields
from django.forms import widgets
from .models import Cliente, Proveedor, Plato, Repartidor,Pedido, Empresa, Carrito
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError



class ProveedorForm(forms.ModelForm):

    nom_proveedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre del proveedor'}))
    rol_local = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Rol del local'}))
    celular = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'+56970932589'}))
    descripcion = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Tu oferta de productos'}))


    def clean_nom_proveedor(self):
        nom_proveedor = self.cleaned_data["nom_proveedor"]
        existe = Proveedor.objects.filter(nom_proveedor__iexact=nom_proveedor).exists()

        if existe:
            raise ValidationError("Este nombre ya existe")

        return nom_proveedor


    class Meta: 
        model = Proveedor
        fields = ['nom_proveedor','rol_local','celular','descripcion']

    

        
class CarritoForm(forms.ModelForm):

    class Meta:
        model = Carrito
        fields = ['idplato', 'cantidad']



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



class GestionEmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ['rut_emp','nom_emp', 'nom_gerente', 'cant_trabajadores','enc_convenio_id_enc_conv']
        labels = {' display:none; '}

    rut_emp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','onkeyup':'formatoRut(this)','placeholder':'Run Empresa'}))
        #fields = 'all'


    #labels = {'rut_emp':'Run Empresa'}
    rut_emp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','onkeyup':'formatoRut(this)','placeholder':'Run Empresa', 'display': None}))
    nom_emp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre Empresa'}))
    nom_gerente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre Gerente'}))
    cant_trabajadores = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Cantidad Trabajadores'}))
    #rut_emp = forms.CharField(max_length=9)    
