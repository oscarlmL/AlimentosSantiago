from django.shortcuts import redirect, render, get_object_or_404
from OrderFood.models import *
from OrderFood.forms import  *


#Modulo Cajero -----------------------------------------------------------------------------
def listar_pedidos_pendientes(request):
    nombre = Cajero.objects.get(email_cajero=request.session['cuentaCajero'])  

    cajero = Cajero.objects.get(email_cajero=request.session['cuentaCajero'])

    print("-----------------------------")
    print(cajero.restaurante_id)

    pedidos_pendientes = Pedido.objects.filter(restaurant_id_restaurante=cajero.restaurante_id, estado='Pendiente').order_by('fecha_pedido','direccion')
    repartidores_disponibles = Repartidor.objects.all()
    data = {
            'pedidos_pendientes':pedidos_pendientes,
            'repartidores_disponibles':repartidores_disponibles,
            'nombre':nombre
            }
    return render(request,'trabajador/cajero/pedidosPendientes.html',data)


def confirmar_pedido(request, id_pedido):

    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    if (request.method == 'GET') and ("confirmar" in request.GET):
        pedido.estado = 'Confirmado'
        pedido.save()
        return redirect('listar-pedidos-pendientes')
    else:
        return redirect('listar-pedidos-pendientes')

def cancelar_pedido(request, id_pedido):

    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    if (request.method == 'GET') and ("cancelar" in request.GET):
        pedido.estado = 'Cancelado'
        pedido.save()
        return redirect('listar-pedidos-pendientes')
    else:
        return redirect('listar-pedidos-pendientes')

def listar_pedidos_confirmados(request):
    nombre = Cajero.objects.get(
        email_cajero=request.session['cuentaCajero'])  
    pedidos_confirmados = Pedido.objects.filter(estado='Confirmado')
    data = {
        'pedidos_confirmados':pedidos_confirmados,
        'nombre':nombre
    }
    return render (request ,'trabajador/cajero/pedidosConfirmados.html',data)

#Fin Modulo Cajero -------------------------------------------------------------------------

