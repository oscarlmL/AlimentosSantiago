from django.urls import path
from .views import *
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('', home, name="home"),
    path('login', Login.as_view(), name="login"),
    path('logout', logout, name="logout"),
    path('generar-cuenta/', auth_middleware(generar_cuenta_enc_cocina) and auth_middleware(generar_cuenta_enc_convenio), name="generar-cuenta"),

]
