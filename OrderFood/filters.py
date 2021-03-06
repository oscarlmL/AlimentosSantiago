from django.db.models.fields import CharField
from django.forms.widgets import Widget
from .models import *
import django_filters
from  django_filters import CharFilter,ChoiceFilter
from django import forms

class buscarPlato(django_filters.FilterSet):
    empty_label_message = '--- Por categoria ---'
    nom_plato = CharFilter(field_name='nom_plato', lookup_expr='icontains')
    categoria = django_filters.ModelChoiceFilter(queryset=categoriaPlato.objects.all(),empty_label=empty_label_message,
    widget=forms.Select(attrs={"class":"form-control"}))
    # Restaurant = django_filters.ModelChoiceFilter(queryset=Restaurant.objects.all(),empty_label=empty_label_message,
    # widget=forms.Select(attrs={"class":"form-control"}))

# class filterTipoPedido(django_filters.FilterSet):
#     tipo_entrega = [
#         ['Delivery','Delivery'],
#         ['Recolectar','Retiro en local']
#     ]
#     tipo_entrega = django_filters.MultipleChoiceFilter(choices=tipo_entrega,
#     widget=forms.Select(attrs={"class":""}))

class buscarPlatoEncCocina(django_filters.FilterSet):
    empty_label_message_categoria = '--- Por categoria ---'
    nom_plato = CharFilter(field_name='nom_plato', lookup_expr='icontains',widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Por nombre del plato"}))
    categoria = django_filters.ModelChoiceFilter(queryset=categoriaPlato.objects.all(),empty_label=empty_label_message_categoria,
    widget=forms.Select(attrs={"class":"form-control"}))