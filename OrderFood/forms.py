from django import forms
from .models import Proveedor, Plato, Repartidor


class ProveedorForm(forms.ModelForm):

    class Meta: 
        model = Proveedor
        fields = ['rol_local', 'nom_proveedor','celular','descripcion']

    rol_local = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nom_proveedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    celular = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class PlatoForm(forms.ModelForm):

    class Meta:
        model = Plato
        fields = '__all__'
        