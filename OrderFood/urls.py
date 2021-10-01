from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('generar-cuenta/', views.generar_cuenta_enc_cocina, name="generar-cuenta"),
]
