from django.urls import path
from .views import *
from .middlewares.auth import auth_middleware,auth_middleware_enc_cocina,auth_middleware_enc_convenio,auth_middleware_repartidor


urlpatterns = [
    path('', home, name="home"),
    path('login', Login.as_view(), name="login"),
    path('logout', logout, name="logout"),

    #CLIENTE
    path('registro/', generarCuentaCliente , name="auto-registro-cliente"),
    path("editar-perfil-cliente/", editar_perfil_cliente, name="editar-perfil-cliente"),

    #ADMINITRACION
    path("editar-perfil/",auth_middleware(editar_perfil_admin),name="editar-perfil"),
    path("cambiar-contraseña/",auth_middleware(cambiar_contraseña_admin),name="cambiar-contraseña"),

    path('gestionar-enc-cocina/', auth_middleware(generar_cuenta_enc_cocina), name="gestionar-encCocina"),
    path('editar-cuenta-enc-cocina/', auth_middleware(editar_cuenta_enc_cocina), name='editar-cuenta-enc-cocina'),
    path('eliminar-cuenta-enc-cocina/', auth_middleware(eliminar_cuenta_enc_cocina), name='eliminar-cuenta-enc-cocina'),

    path('gestionar-enc-convenio', generar_cuenta_enc_convenio, name="gestionar-enc-convenio"),
    path('editar-cuenta-enc-convenio/', auth_middleware(editar_cuenta_enc_convenio), name='editar-cuenta-enc-convenio'),
    path('eliminar-cuenta-enc-convenio/', auth_middleware(eliminar_cuenta_enc_convenio), name='eliminar-cuenta-enc-convenio'),


    path('gestionar-repartidor/', auth_middleware(generar_cuenta_repartidor), name='gestionar-repartidor'),
    path('editar-cuenta-repartidor/', auth_middleware(editar_cuenta_repartidor), name='editar-cuenta-repartidor'),
    path('eliminar-cuenta-repartidor/', auth_middleware(eliminar_cuenta_repartidor), name='eliminar-cuenta-repartidor'),
    #FIN ADMINITRACION

    #ENCARGADO COCINA
    path("editar-perfil-enc-cocina/",auth_middleware_enc_cocina(editar_perfil_enc_cocina),name="editar-perfil-enc-cocina"),
    path("cambiar-contraseña-enc-cocina/",auth_middleware_enc_cocina(cambiar_contraseña_enc_cocina),name="cambiar-contraseña-enc-cocina"),
    path('gestionar-plato/', auth_middleware_enc_cocina(gestionar_plato), name="gestionar-plato"),
    path('modificar-plato/', auth_middleware_enc_cocina(modificar_plato), name="modificar_plato"),
    path('eliminar-plato/', auth_middleware_enc_cocina(eliminar_plato), name="eliminar_plato"),
    #path Proveedor
    path('proveedor', proveedor, name="proveedor"),
    path('listar-proveedor/', auth_middleware_enc_cocina(listar_proveedor), name="listar_proveedor"),
    path('modificar-proveedor/', auth_middleware_enc_cocina(modificar_proveedor), name="modificar_proveedor"),
    path('eliminar-proveedor/', auth_middleware_enc_cocina(eliminar_proveedor), name="eliminar_proveedor"),
    #End Path
    #FIN ENCARGADO COCINA

    #ENCARGADO CONVENIO
    path("editar-perfil-enc-convenio/",auth_middleware_enc_convenio(editar_perfil_enc_convenio),name="editar-perfil-enc-convenio"),
    path("cambiar-contraseña-enc-convenio/",auth_middleware_enc_convenio(cambiar_contraseña_enc_convenio),name="cambiar-contraseña-enc-convenio"),
    path('gestionar-empresa/', auth_middleware_enc_convenio(agregar_empresa) , name='gestionar-empresa'),
    path('modificar-convenio/<rut_emp>/', modificar_convenio, name='modificar_convenio'),
    path('eliminar-empresa//<slug:rut_emp>/', eliminar_empresa, name='eliminar-empresa'),
    path('generar-cuenta-empleado/', auth_middleware_enc_convenio(generar_cuenta_empleado), name='generar-cuenta-empleado'),
    path('editar-cuentaTrabEmp', auth_middleware_enc_convenio(editar_cuenta_trab_emp), name='editar-cuentaTrabEmp'),
    path('eliminar-cuentaTrabEmp/<id>/', eliminar_cuenta_trab_emp, name='eliminar-cuentaTrabEmp'),
    #FIN ENCARGADO CONVENIO


    #REPARTIDOR
    path("editar-perfil-repartidor/",auth_middleware_repartidor(editar_perfil_repartidor),name="editar-perfil-repartidor"),
    path("cambiar-contraseña-repartidor/",auth_middleware_repartidor(cambiar_contraseña_repartidor),name="cambiar-contraseña-repartidor"),
    #FIN REPARTIDOR


    #path Pedidos
    path('agregar-pedido/', agregar_pedido, name="agregar_pedido"),
    path('listar-pedido/', listar_pedido, name="listar_pedido"),
    path('modificar-pedido/<id>/', modificar_pedido, name="modificar_pedido"),
    path('eliminar-pedido/<id>/', eliminar_pedido, name="eliminar_pedido"),
    #End Path

    
]
