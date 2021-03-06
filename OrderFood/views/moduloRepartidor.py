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


def cambiar_contraseña_repartidor(request):
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
        contraseña_actual = request.POST['contraseña_actual']
        contraseña1 = request.POST['nueva_contraseña']
        contraseña2 = request.POST['con_nueva_contraseña']
        cuentaRepartidor = Repartidor.get_repartidor_by_id(email)
        if cuentaRepartidor:
            flag = check_password(
                contraseña_actual, cuentaRepartidor.contraseña1)
            error_message = None
            if flag:
                repartidor = Repartidor.objects.get(
                    id_repartidor=request.session['cuentaRepartidor'])
                repartidor.contraseña1 = contraseña1
                repartidor.contraseña2 = contraseña2

                error_message = None
                if len(contraseña1 and contraseña2) < 5:
                    error_message = 'Las contraseñas deben tener mas de 5 caracteres'
                elif len(contraseña1 and contraseña2) > 10:
                    error_message = 'Las contraseñas no pueden tener más de 10 caracteres'
                elif contraseña2 != contraseña1:
                    error_message = 'Las contraseñas no coinciden'

                if not error_message:
                    repartidor.contraseña1 = make_password(
                        repartidor.contraseña1)
                    repartidor.contraseña2 = make_password(
                        repartidor.contraseña2)
                    repartidor.save()
                    messages.success(
                        request, "Contraseña Cambiada Correctamente")
                    return redirect('cambiar-contraseña-repartidor')
                else:
                    nombre = Repartidor.objects.get(
                        id_repartidor=request.session['cuentaRepartidor'])
                    data = {
                        'nombre': nombre,
                        'error': error_message,

                    }
                return render(request, 'trabajador/repartidor/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                nombre = Repartidor.objects.get(
                        id_repartidor=request.session['cuentaRepartidor'])
                data = {
                    'nombre': nombre,
                    'error': error_message,

                }
            return render(request, 'trabajador/repartidor/cambiar_contraseña.html', data)
    return render(request, "trabajador/repartidor/cambiar_contraseña.html", data)


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
