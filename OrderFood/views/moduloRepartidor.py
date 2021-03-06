from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from OrderFood.models import *
from OrderFood.forms import  *
from django.conf import settings

# Modulo repartidor
def editar_perfil_repartidor(request):
    check = Repartidor.objects.filter(
        id_repartidor=request.session['cuentaRepartidor'])
    if len(check) > 0:
        nombre = Repartidor.objects.get(
            id_repartidor=request.session['cuentaRepartidor'])
        repartidor = Repartidor.objects.get(
            id_repartidor=request.session['cuentaRepartidor'])
        data = {'repartidor': repartidor,'nombre':nombre}
    if request.method == 'POST':
        rut_repartidor = request.POST["rut_repartidor"]
        nombre_repartidor = request.POST["nombre_repartidor"]
        apellido_repartidor = request.POST["apellido_repartidor"]
        email_repartidor = request.POST["email_repartidor"]
        tipo_veh = request.POST["tipo_veh"]
        celular = request.POST["celular"]

        repartidor = Repartidor.objects.get(
            id_repartidor=request.session['cuentaRepartidor'])
        repartidor.rut_repartidor = rut_repartidor
        repartidor.nombre_repartidor = nombre_repartidor
        repartidor.apellido_repartidor = apellido_repartidor
        repartidor.email_repartidor = email_repartidor
        repartidor.tipo_veh = tipo_veh
        repartidor.celular = celular

        error_message = None
        if(not repartidor.rut_repartidor):
            error_message = 'El Rut es requerido'
        elif not repartidor.nombre_repartidor:
            error_message = 'El Nombre es requerido'
        elif not repartidor.apellido_repartidor:
            error_message = 'El Apellido es requerido'
        elif not repartidor.email_repartidor:
            error_message = 'El Email es requerido'
        elif not repartidor.tipo_veh:
            error_message = 'El tipo de vehiculo es requerido'
        elif not repartidor.celular:
            error_message = 'El celular es requerido'
        elif len(repartidor.celular) > 9:
            error_message = 'El Celular no puede tener mas de 9 digitos'

        # guardar datos de cuenta
        if not error_message:
            repartidor.save()
            messages.success(request, "Datos editados correctamente")
            return redirect('editar-perfil-repartidor')
        else:
            nombre = Repartidor.objects.get(
                id_repartidor=request.session['cuentaRepartidor'])
            data = {
                'error': error_message,
                'repartidor':repartidor,
                'nombre':nombre
            }
    return render(request, 'trabajador/repartidor/editarPerfil.html', data)


def cambiar_contrase??a_repartidor(request):
    check = Repartidor.objects.filter(
        id_repartidor=request.session['cuentaRepartidor'])
    if len(check) > 0:
        email = request.session['cuentaRepartidor']
        nombre = Repartidor.objects.get(
            id_repartidor=request.session['cuentaRepartidor'])
        repartidor = Repartidor.objects.get(
            id_repartidor=request.session['cuentaRepartidor'])
        data = {'email': email,'repartidor':repartidor,'nombre':nombre}
    if request.method == "POST":
        contrase??a_actual = request.POST['contrase??a_actual']
        contrase??a1 = request.POST['nueva_contrase??a']
        contrase??a2 = request.POST['con_nueva_contrase??a']
        cuentaRepartidor = Repartidor.get_repartidor_by_id(email)
        if cuentaRepartidor:
            flag = check_password(
                contrase??a_actual, cuentaRepartidor.contrase??a1)
            error_message = None
            if flag:
                repartidor = Repartidor.objects.get(
                    id_repartidor=request.session['cuentaRepartidor'])
                repartidor.contrase??a1 = contrase??a1
                repartidor.contrase??a2 = contrase??a2

                error_message = None
                if len(contrase??a1 and contrase??a2) < 5:
                    error_message = 'Las contrase??as deben tener mas de 5 caracteres'
                elif len(contrase??a1 and contrase??a2) > 10:
                    error_message = 'Las contrase??as no pueden tener m??s de 10 caracteres'
                elif contrase??a2 != contrase??a1:
                    error_message = 'Las contrase??as no coinciden'

                if not error_message:
                    repartidor.contrase??a1 = make_password(
                        repartidor.contrase??a1)
                    repartidor.contrase??a2 = make_password(
                        repartidor.contrase??a2)
                    repartidor.save()
                    messages.success(
                        request, "Contrase??a Cambiada Correctamente")
                    return redirect('cambiar-contrase??a-repartidor')
                else:
                    nombre = Repartidor.objects.get(
                        id_repartidor=request.session['cuentaRepartidor'])
                    data = {
                        'nombre': nombre,
                        'error': error_message,

                    }
                return render(request, 'trabajador/repartidor/cambiar_contrase??a.html', data)
            else:
                error_message = 'La contrase??a actual es incorrecta'
                nombre = Repartidor.objects.get(
                        id_repartidor=request.session['cuentaRepartidor'])
                data = {
                    'nombre': nombre,
                    'error': error_message,

                }
            return render(request, 'trabajador/repartidor/cambiar_contrase??a.html', data)
    return render(request, "trabajador/repartidor/cambiar_contrase??a.html", data)


#pedidos confirmados
def listar_pedidos_activos(request):
    nombre = Repartidor.objects.get(id_repartidor=request.session['cuentaRepartidor'])
    pedidos_confirmados = Pedido.objects.filter(estado='Confirmado',tipo_entrega='Delivery')
    data = {
        'pedidos_confirmados':pedidos_confirmados,
        'nombre':nombre
    }
    return render (request ,'trabajador/repartidor/pedidos_activos_local.html',data)


def aceptar_pedido(request, id_pedido):
    repartidor = request.session.get('cuentaRepartidor')
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    pedido_repartidor = get_object_or_404(Repartidor, id_repartidor=repartidor)
    if (request.method == 'GET') and ("aceptar" in request.GET):
        pedido.estado = 'En ruta'
        pedido.repartidor_id = pedido_repartidor
        pedido.save()
        return redirect('listar-pedidos-aceptados')
    else:
        return redirect('listar-pedidos-activos')



def entregar_pedido(request, id_pedido):
     pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
     if (request.method == 'GET') and ("entregar" in request.GET):
         pedido.estado = 'Entregado'
         pedido.save()
         return redirect('listar-pedidos-activos')
     else:
         return redirect('listar-pedidos-activos')

def cancelar_pedido(request, id_pedido):
     pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
     if (request.method == 'GET') and ("cancelar" in request.GET):
         pedido.estado = 'No entregado'
         pedido.save()
         return redirect('listar-pedidos-activos')
     else:
         return redirect('listar-pedidos-activos')

#pedidos aceptados
def listar_pedidos_aceptados(request):
    repartidor = Repartidor.objects.get(id_repartidor=request.session['cuentaRepartidor'])
    pedidos_aceptados = Pedido.objects.filter(estado='En ruta', repartidor_id = repartidor)
    pedidos_aceptados1 = Pedido.objects.filter(estado='En ruta', repartidor_id = repartidor)
    data = {
        'pedidos_aceptados': pedidos_aceptados,
        'pedidos_aceptados1':pedidos_aceptados1,
        'repartidor':repartidor,
    }
    print('a',pedidos_aceptados1)
    return render (request ,'trabajador/repartidor/pedidos_aceptados.html',data)
# Fin Modulo repartidor
