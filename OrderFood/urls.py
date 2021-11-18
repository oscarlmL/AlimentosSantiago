from django.urls import path
from .views import *
from .middlewares.auth import auth_middleware,auth_middleware_enc_cocina,auth_middleware_enc_convenio,auth_middleware_repartidor,auth_middleware_cliente


urlpatterns = [
    path('ubicacion', ubicacion, name="ubicacion"),
    path('', home.as_view(), name="home"),
    path('home', incio_trabajdor, name="incio_trabajdor"),

    path('platos/<int:id_restaurante>/',home.as_view() and listar_plato_restaurante, name='platos'),




    path('login', Login.as_view(), name="login"),
    path('logout', logout, name="logout"),

    #CLIENTE
    path('registro/', generarCuentaCliente , name="auto-registro-cliente"),
    path("editar-perfil-cliente/", auth_middleware_cliente(editar_perfil_cliente), name="editar-perfil-cliente"),
    path("cambiar-contraseña-cliente/",auth_middleware_cliente(cambiar_contraseña_cliente),name="cambiar-contraseña-cliente"),
    path('realizar-pedido', auth_middleware_cliente(realizar_pedido.as_view()), name="realizar-pedido"),
    path('pagar', auth_middleware_cliente(realizar_pedido.as_view()), name="pagar"),
    path('mis-pedidos', auth_middleware_cliente(pedidos.as_view()), name="mis-pedidos"),

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

    path('gestionar-cajero/', auth_middleware(generar_cuenta_cajero), name='gestionar-cajero'),
    path('editar-cuenta-cajero/', auth_middleware(editar_cuenta_cajero), name='editar-cuenta-cajero'),
    path('eliminar-cuenta-cajero/', auth_middleware(eliminar_cuenta_cajero), name='eliminar-cuenta-cajero'),
    #FIN ADMINITRACION

    #ENCARGADO COCINA
    path("editar-perfil-enc-cocina/",auth_middleware_enc_cocina(editar_perfil_enc_cocina),name="editar-perfil-enc-cocina"),
    path("cambiar-contraseña-enc-cocina/",auth_middleware_enc_cocina(cambiar_contraseña_enc_cocina),name="cambiar-contraseña-enc-cocina"),
    #path Platos
    path('gestionar-plato/', auth_middleware_enc_cocina(gestionar_plato), name="gestionar-plato"),
    path('modificar-plato/', auth_middleware_enc_cocina(modificar_plato), name="modificar_plato"),
    path('eliminar-plato/', auth_middleware_enc_cocina(eliminar_plato), name="eliminar_plato"),
    path('buscar-plato/', (buscar_plato), name="buscar-plato"),

    #path Proveedor
    path('proveedor', proveedor, name="proveedor"),
    path('listar-proveedor/', auth_middleware_enc_cocina(listar_proveedor), name="listar_proveedor"),
    path('modificar-proveedor/', auth_middleware_enc_cocina(modificar_proveedor), name="modificar_proveedor"),
    path('eliminar-proveedor/', auth_middleware_enc_cocina(eliminar_proveedor), name="eliminar_proveedor"),
    #path Restaurant
    path('restaurant', restaurant, name="restaurant"),
    path('listar-restaurant/', auth_middleware_enc_cocina(listar_restaurant), name="listar-restaurant"),
    path('modificar-restaurant/', auth_middleware_enc_cocina(modificar_restaurant), name="modificar-restaurant"),
    path('eliminar-restaurant/', auth_middleware_enc_cocina(eliminar_restaurant), name="eliminar-restaurant"),
    

    #FIN ENCARGADO COCINA

    #ENCARGADO CONVENIO
    path("editar-perfil-enc-convenio/",auth_middleware_enc_convenio(editar_perfil_enc_convenio),name="editar-perfil-enc-convenio"),
    path("cambiar-contraseña-enc-convenio/",auth_middleware_enc_convenio(cambiar_contraseña_enc_convenio),name="cambiar-contraseña-enc-convenio"),
    path('gestionar-empresa/', auth_middleware_enc_convenio(agregar_empresa) , name='gestionar-empresa'),
    path('modificar-convenio/<rut_emp>/', modificar_convenio, name='modificar_convenio'),
    path('eliminar-empresa//<slug:rut_emp>/', eliminar_empresa, name='eliminar-empresa'),
    path('generar-cuenta-empleado/', auth_middleware_enc_convenio(generar_cuenta_empleado), name='generar-cuenta-empleado'),
    path('gestionar-empresa/listar-cuentas-empleados/', listar_cuenta_empleados, name='listar-cuentas-empleados'),

    path('editar-cuentaTrabEmp', auth_middleware_enc_convenio(editar_cuenta_trab_emp), name='editar-cuentaTrabEmp'),
    path('eliminar-cuentaTrabEmp/<id>/', eliminar_cuenta_trab_emp, name='eliminar-cuentaTrabEmp'),
    #FIN ENCARGADO CONVENIO


    #REPARTIDOR
    path('editar-perfil-repartidor/',auth_middleware_repartidor(editar_perfil_repartidor),name="editar-perfil-repartidor"),
    path('cambiar-contraseña-repartidor/',auth_middleware_repartidor(cambiar_contraseña_repartidor),name="cambiar-contraseña-repartidor"),
    path('listar-pedidos-activos/',auth_middleware_repartidor(listar_pedidos_activos),name="listar-pedidos-activos"),
    path('aceptar-pedido/<int:id_pedido>/',aceptar_pedido,name="aceptar-pedido"),
    path('listar-pedidos-aceptados',auth_middleware_repartidor(listar_pedidos_aceptados),name="listar-pedidos-aceptados"),
    path('entregar-pedido/<int:id_pedido>/',entregar_pedido,name="entregar-pedido"),


    #FIN REPARTIDOR


    #path Pedidos
    path('agregar-pedido/', agregar_pedido, name="agregar_pedido"),
    path('listar-pedido/', listar_pedido, name="listar_pedido"),
    path('modificar-pedido/<id>/', modificar_pedido, name="modificar_pedido"),
    path('eliminar-pedido/<id>/', eliminar_pedido, name="eliminar_pedido"),
    #End Path

    #path CAJERO
    path('listar-pedidos-pendientes/',listar_pedidos_pendientes, name="listar-pedidos-pendientes"),
    path('confirmar-pedido/<int:id_pedido>/',confirmar_pedido, name="confirmar-pedido"),
    path('listar-pedidos-confirmados/',listar_pedidos_confirmados, name="listar-pedidos-confirmados")
    
    #END CAJERO

 
    # path('agregar_carrito', agregar_carrito, name= 'agregar_carrito'),
    # path('listar_carrito', listar_carrito, name='listar_carrito'),
    # path('eliminar_item_carrito/<id>/', eliminar_item_carrito, name='eliminar_item_carrito'),   
]
