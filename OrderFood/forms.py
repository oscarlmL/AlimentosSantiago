from django import forms
import django
from django.db.models import fields
from django.forms import widgets
from .models import Cliente, Proveedor, Plato, Repartidor, Pedido, Empresa, Carrito, Restaurant
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


#MOD RESTAURANT
class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['nombre_rest', 'direccion_rest', 'imagen']
    nombre_rest = forms.CharField(max_length=49, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre del restaurant'}), label='Nombre del Restaurant')
    direccion_rest = forms.CharField(max_length=49, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id':'clientAddress', 'placeholder': 'Ej: Novena 849'}), label='Dirección')
    # comuna_rest = forms.CharField(max_length=49, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Ej: Valparaiso, Quilpué'}), label='Comuna')
    imagen = forms.ImageField()

    # def clean_comuna_rest(self):
    #     nombre = self.cleaned_data['comuna_rest']
    #     if not nombre.isalpha():
    #         raise forms.ValidationError('La comuna no puede contener números')
    #     return nombre

#MOD PROVEEDOR
class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = ['nom_proveedor', 'rol_local', 'celular', 'descripcion']
    nom_proveedor = forms.CharField(max_length=49, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}), label='Nombre del Proveedor')
    rol_local = forms.CharField(max_length=49, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ej: comida china, japonesa, peruana, insumos'}), label='Rol del Local')
    celular = forms.CharField(min_length=9, max_length=9, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'tu celular ej: 977079248'}), label='Celular de Contacto')
    descripcion = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Tu oferta de productos, empresa, dirección'}), label='Descripción de la oferta a realizar')

# Validación solo numeros
    def clean_celular(self):
        nombre = self.cleaned_data['celular']
        if not nombre.isdigit():
            raise forms.ValidationError('El celular no puede contener letras ni simbolos')
        return nombre

#MOD PEDIDO
class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            "fecha_pedido": forms.SelectDateWidget()
        }

#MOD PLATO
class PlatoForm(forms.ModelForm):

    class Meta:
        model = Plato
        fields = ['categoria','nom_plato', 'descripcion', 'valor_plato', 'Imagen','Restaurant']
    nom_plato = forms.CharField(max_length=49, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre del plato'}), label='Nombre del Plato')
    descripcion = forms.CharField(max_length=49, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Descripción'}), label='Descripción')
    valor_plato = forms.CharField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Valor del plato'}), label='Precio')
    Imagen = forms.ImageField()

# Validación solo numeros
    def clean_valor_plato(self):
        nombre = self.cleaned_data['valor_plato']
        if not nombre.isnumeric():
            raise forms.ValidationError('El valor no puede contener letras')
        return nombre

#MOD REPARTIDOR
class RepartidorForm(forms.ModelForm):

    class Meta:
        model = Repartidor
        fields = ['rut_repartidor', 'nombre_repartidor', 'apellido_repartidor',
                  'email_repartidor', 'patente_veh', 'celular', 'contraseña1', 'contraseña2']


class GestionEmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ['rut_emp',
                  'nom_emp',
                  'nom_gerente',
                  'cant_trabajadores',
                  ]

    rut_emp = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'onkeyup': 'formatoRut(this)', 'placeholder': 'Run Empresa', 'display': None}), label='Run Empresa')
    nom_emp = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre Empresa'}), label='Nombre de la Empresa')
    nom_gerente = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre Gerente'}), label='Nombre del Gerente')
    cant_trabajadores = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Cantidad Trabajadores'}), label='Cantidad de Trabajadores')
    


# INFORMACIÓN VALIDACIONES
# Check if a string contains only decimal: str.isdecimal()
# Check if a string contains only digits: str.isdigit()
# Check if a string contains only numeric: str.isnumeric()
# Check if a string contains only alphabetic: str.isalpha()
# Check if a string contains only alphanumeric: str.isalnum()
# Check if a string contains only ASCII: str.isascii()
# Check if a string is empty
# Check if a string is a number (= can be converted to numeric value)

# INFORMACIÓN VALIDAR SIN REPETIR EL NOMBRE
 # def clean_nom_proveedor(self):
    #nom_proveedor = self.cleaned_data["nom_proveedor"]
    #existe = Proveedor.objects.filter(nom_proveedor__iexact=nom_proveedor).exists()

    # if existe:
    #raise ValidationError("Este nombre ya existe")

    # return nom_proveedor