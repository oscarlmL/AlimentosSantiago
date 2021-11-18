from django.shortcuts import redirect, render, get_object_or_404
from OrderFood.models import *
from OrderFood.forms import  *


#Modulo Cajero -----------------------------------------------------------------------------
def listar_pedidos_pendientes(request):
    pedidos_pendientes = Pedido.objects.filter(estado='Pendiente')
    repartidores_disponibles = Repartidor.objects.all()
    data = {
            'pedidos_pendientes':pedidos_pendientes,
            'repartidores_disponibles':repartidores_disponibles
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

def listar_pedidos_confirmados(request):
    pedidos_confirmados = Pedido.objects.filter(estado='Confirmado')
    data = {
        'pedidos_confirmados':pedidos_confirmados
    }
    return render (request ,'trabajador/cajero/pedidosConfirmados.html',data)
#Fin Modulo Cajero -------------------------------------------------------------------------

