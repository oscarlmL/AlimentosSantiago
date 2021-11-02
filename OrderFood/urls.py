from django.urls import path
from .views import *
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('', home, name="home"),
    path('login', Login.as_view(), name="login"),
    path('logout', logout, name="logout"),

    path('registro/', registro, name="registro"),
    path("editar-perfil/",auth_middleware(editar_perfil_admin),name="editar-perfil"),
    path("editar-perfil-enc-cocina/",editar_perfil_enc_cocina,name="editar-perfil-enc-cocina"),
    path("editar-perfil-enc-convenio/",editar_perfil_enc_convenio,name="editar-perfil-enc-convenio"),
    path("editar-perfil-repartidor/",editar_perfil_repartidor,name="editar-perfil-repartidor"),

    path("cambiar-contraseña/",cambiar_contraseña_admin,name="cambiar-contraseña"),


    path('gestionar-enc-cocina/', auth_middleware(generar_cuenta_enc_cocina), name="gestionar-encCocina"),
    path('editar-cuenta-enc-cocina/', auth_middleware(editar_cuenta_enc_cocina), name='editar-cuenta-enc-cocina'),
    path('eliminar-cuenta-enc-cocina/<id_enc_coc>/', eliminar_cuenta_enc_cocina, name='eliminar-cuenta-enc-cocina'),

    path('gestionar-enc-convenio', auth_middleware(generar_cuenta_enc_convenio), name="gestionar-enc-convenio"),
    path('editar-cuenta-enc-convenio/', auth_middleware(editar_cuenta_enc_convenio), name='editar-cuenta-enc-convenio'),
    path('eliminar-cuenta-enc-convenio/<id_enc_conv>/', eliminar_cuenta_enc_convenio, name='eliminar-cuenta-enc-convenio'),


    path('gestionar-repartidor/', auth_middleware(generar_cuenta_repartidor), name='gestionar-repartidor'),
    path('editar-cuenta-repartidor/', auth_middleware(editar_cuenta_repartidor), name='editar-cuenta-repartidor'),
    path('eliminar-cuenta-repartidor/<id_repartidor>/', eliminar_cuenta_repartidor, name='eliminar-cuenta-repartidor'),

    #path Proveedor
    path('proveedor', proveedor, name="proveedor"),
    path('listar-proveedor/', listar_proveedor, name="listar_proveedor"),
    path('modificar-proveedor/<id>/', modificar_proveedor, name="modificar_proveedor"),
    path('eliminar-proveedor/<id>/', eliminar_proveedor, name="eliminar_proveedor"),
    #End Path

    #path Pedidos
    path('agregar-pedido/', agregar_pedido, name="agregar_pedido"),
    path('listar-pedido/', listar_pedido, name="listar_pedido"),
    path('modificar-pedido/<id>/', modificar_pedido, name="modificar_pedido"),
    path('eliminar-pedido/<id>/', eliminar_pedido, name="eliminar_pedido"),
    #End Path

    path('agregar-plato/', agregar_plato, name="agregar_plato"),
    path('listar-platos/', listar_platos, name='listar_plato'),
    path('modificar-plato/<id_plato>/', modificar_plato, name="modificar_plato"),
    path('eliminar-plato/<id_plato>/', eliminar_plato, name="eliminar_plato"),
    #path('repartidor', repartidor, name="repartidor"),
 
    #path encargadoEmpresasConvenio
    path('agregar-empresa', agregar_empresa , name='agregar_empresa'),
    path('listar-empresa', listar_empresa, name='listar_empresa'),
    path('modificar-convenio/<rut_emp>/', modificar_convenio, name='modificar_convenio'),
    path('eliminar-empresa/<rut_emp>/', eliminar_empresa, name='eliminar_empresa'),

    path('agregar_carrito', agregar_carrito, name= 'agregar_carrito'),
    path('listar_carrito', listar_carrito, name='listar_carrito'),
    path('eliminar_item_carrito/<id>/', eliminar_item_carrito, name='eliminar_item_carrito'),   
]
