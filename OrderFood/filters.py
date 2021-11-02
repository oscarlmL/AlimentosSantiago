from django.db.models.fields import CharField
from .models import *
import django_filters
from  django_filters import CharFilter,ChoiceFilter
from django import forms

class buscarPlato(django_filters.FilterSet):
    empty_label_message = '--- Buscar por Restaurante ---'
    nom_plato = CharFilter(field_name='nom_plato', lookup_expr='icontains', widget=forms.TextInput(attrs={"class":"form-control rounded","placeholder":"Buscar por nombre del Plato"}))
    # Restaurant = django_filters.ModelChoiceFilter(queryset=Restaurant.objects.all(),empty_label=empty_label_message,
    # widget=forms.Select(attrs={"class":"form-control"}))