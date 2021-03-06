from django.urls import path
from .views import *
from OrderFood.views.home import *
from OrderFood.views.moduloAdministrador import *
from OrderFood.views.moduloCajero import *
from OrderFood.views.moduloCliente import *
from OrderFood.views.moduloEncCocina import *
from OrderFood.views.moduloEncConvenio import *
from OrderFood.views.moduloRepartidor import *


from .middlewares.auth import auth_middleware,auth_middleware_enc_cocina,auth_middleware_enc_convenio,auth_middleware_repartidor,auth_middleware_cliente,auth_middleware_cajero


urlpatterns = [
    path('', home.as_view(), name="home"),
    path('home', incio_trabajador, name="incio_trabajador"),

    path('platos/<int:id_restaurante>/',home.as_view() and listar_plato_restaurante, name='platos'),

    path('login', Login.as_view(), name="login"),
    path('logout', logout, name="logout"),

    path('eliminar-plato-carro/', eliminar_plato_carro,name="eliminar-plato-carro"),
    path('limpiar-carro/', limpiar_carro,name="limpiar-carro"),


    #CLIENTE
    path('registro/', generarCuentaCliente , name="auto-registro-cliente"),
    path("editar-perfil-cliente/", auth_middleware_cliente(editar_perfil_cliente), name="editar-perfil-cliente"),
    path("cambiar-contraseña-cliente/",auth_middleware_cliente(cambiar_contraseña_cliente),name="cambiar-contraseña-cliente"),
    path('realizar-pedido', auth_middleware_cliente(realizar_pedido.as_view()), name="realizar-pedido"),
    path('pagar', auth_middleware_cliente(realizar_pedido.as_view()), name="pagar"),
    path('webpay', webpay, name="webpay"),
    path('terminar', webpaycommit, name="terminar"),


    path('mis-pedidos', auth_middleware_cliente(pedidos.as_view()), name="mis-pedidos"),
    path('historial-pedidos', auth_middleware_cliente(historial_pedidos.as_view()), name="historial-pedidos"),


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
    path('eliminar-plato/', auth_middleware_enc_cocina(eliminar_plato), name="eliminar-plato"),
    # path('buscar-plato/', (buscar_plato), name="buscar-plato"),

    #path Proveedor
    path('proveedor',proveedor, name="proveedor"),
    path('listar-proveedor/', auth_middleware_enc_cocina(listar_proveedor), name="listar-proveedor"),
    path('modificar-proveedor/', auth_middleware_enc_cocina(modificar_proveedor), name="modificar-proveedor"),
    path('eliminar-proveedor/', auth_middleware_enc_cocina(eliminar_proveedor), name="eliminar-proveedor"),
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
    path('eliminar-empresa/', eliminar_empresa, name='eliminar-empresa'),
    path('generar-cuenta-empleado/', auth_middleware_enc_convenio(generar_cuenta_empleado), name='generar-cuenta-empleado'),
    path('gestionar-empresa/listar-cuentas-empleados/', listar_cuenta_empleados, name='listar-cuentas-empleados'),
    path("registrarsaldo/", cargar_saldo_cliente , name="registrarsaldo"),
    path("leertxt", leertxt , name="leertxt"),

    path('editar-cuentaTrabEmp/', auth_middleware_enc_convenio(editar_cuenta_trab_emp), name='editar-cuentaTrabEmp'),
    path('eliminar-cuentaTrabEmp/', eliminar_cuenta_trab_emp, name='eliminar-cuentaTrabEmp'),
    #FIN ENCARGADO CONVENIO


    #REPARTIDOR
    path('editar-perfil-repartidor/',auth_middleware_repartidor(editar_perfil_repartidor),name="editar-perfil-repartidor"),
    path('cambiar-contraseña-repartidor/',auth_middleware_repartidor(cambiar_contraseña_repartidor),name="cambiar-contraseña-repartidor"),
    path('listar-pedidos-activos/',auth_middleware_repartidor(listar_pedidos_activos),name="listar-pedidos-activos"),
    path('aceptar-pedido/<int:id_pedido>/',aceptar_pedido,name="aceptar-pedido"),
    path('listar-pedidos-aceptados',auth_middleware_repartidor(listar_pedidos_aceptados),name="listar-pedidos-aceptados"),
    path('entregar-pedido/<int:id_pedido>/',entregar_pedido,name="entregar-pedido"),
    path('cancelar-pedido/<int:id_pedido>/',cancelar_pedido,name="cancelar-pedido"),

    #FIN REPARTIDOR


    #path Pedidos
    path('agregar-pedido/', agregar_pedido, name="agregar-pedido"),
    path('listar-pedido/', listar_pedido, name="listar-pedido"),
    path('modificar-pedido/<id>/', modificar_pedido, name="modificar-pedido"),
    path('eliminar-pedido/<id>/', eliminar_pedido, name="eliminar-pedido"),
    #End Path

    #path CAJERO
    path('listar-pedidos-pendientes/',auth_middleware_cajero(listar_pedidos_pendientes), name="listar-pedidos-pendientes"),
    path('confirmar-pedido/<int:id_pedido>/',confirmar_pedido, name="confirmar-pedido"),
    path('listar-pedidos-confirmados/',auth_middleware_cajero(listar_pedidos_confirmados), name="listar-pedidos-confirmados"),
    path('cancelar-pedido-cajero/<int:id_pedido>/',cancelar_pedido_cajero, name="cancelar-pedido-cajero"),
    
    #END CAJERO
    # path('agregar_carrito', agregar_carrito, name= 'agregar_carrito'),
    # path('listar_carrito', listar_carrito, name='listar_carrito'),
    # path('eliminar_item_carrito/<id>/', eliminar_item_carrito, name='eliminar_item_carrito'),   
]
