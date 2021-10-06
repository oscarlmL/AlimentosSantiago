from django.urls import path
from .views import *
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('', home, name="home"),
    path('login', Login.as_view(), name="login"),
    path('logout', logout, name="logout"),
    path('generar-cuenta/',generar_cuenta_get, name="generar-cuenta"),
    path('generar-cuenta/encargado-cocina', auth_middleware(generar_cuenta_enc_cocina), name="encargado-cocina"),
    path('generar-cuenta/encargado-convenio', auth_middleware(generar_cuenta_enc_convenio), name="encargado-convenio"),
    path('generar-cuenta/repartidor', auth_middleware(generar_cuenta_repartidor), name="repartidor"),
    path('proveedor', proveedor, name="proveedor"),
    path('agregar-plato/', agregar_plato, name="agregar_plato"),
    path('listar-platos/', listar_platos, name='listar_plato'),
    path('modificar-plato/<id_plato>/', modificar_plato, name="modificar_plato"),
    path('eliminar-plato/<id_plato>/', eliminar_plato, name="eliminar_plato"),
    
]
