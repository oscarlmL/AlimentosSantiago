from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django import views
from OrderFood.forms import  *
from OrderFood.models import  *
from django.views import View
from django.contrib import messages
from django.db.models import Q


# Modulo Cliente
def generarCuentaCliente(request):
    if request.method == 'GET':
        return render(request, 'cliente/autoRegistroCliente.html')
    else:
        nombre_cli = request.POST["nombre_cli"]
        apaterno_cli = request.POST["apaterno_cli"]
        amaterno_cli = request.POST["amaterno_cli"]
        fono_cli = request.POST["fono_cli"]
        email_cli = request.POST["email_cli"]
        #saldo_cli = postData.get('')
        #empresa_rut_empresa = request.POST['empresa_rut_empresa']
        contraseña1 = request.POST["contraseña1"]
        contraseña2 = request.POST["contraseña2"]

        # validaciones
        value = {
            'nombre_cli': nombre_cli,
            'apaterno_cli': apaterno_cli,
            'amaterno_cli': amaterno_cli,
            'fono_cli': fono_cli,
            'email_cli': email_cli,
            'contraseña1': contraseña1,
            'contraseña2': contraseña2,
        }
        error_message = None
        cliente = Cliente(nombre_cli=nombre_cli,
                          apaterno_cli=apaterno_cli,
                          amaterno_cli=amaterno_cli,
                          fono_cli=fono_cli,
                          email_cli=email_cli,
                          contraseña1=contraseña1,
                          contraseña2=contraseña2)

        if not nombre_cli:
            error_message = 'El Nombre es requerido'
        elif len(nombre_cli) < 4:
            error_message = 'El Nombre debe tener mas de 4 caracteres'
        elif not apaterno_cli:
            error_message = 'El Apellido Paterno es requerido'
        elif len(apaterno_cli) < 2:
            error_message = 'El apellido debe tener mas de 2 caracteres'
        elif not amaterno_cli:
            error_message = 'El Apellido Materno es requerido'
        elif len(amaterno_cli) < 2:
            error_message = 'El Apellido debe tener mas de 2 caracteres'
        elif not fono_cli:
            error_message = 'El Telefono es requerido'
        elif len(fono_cli) < 7:
            error_message = 'El Telefono debe tener mas de 7 digitos'
        elif not email_cli:
            error_message = 'El Email es requerido'
        elif len(contraseña1 and contraseña2) < 5:
            error_message = 'Las contraseñas deben tener mas de 5 caracteres'

        elif len(contraseña1 and contraseña2) > 10:
            error_message = 'Las contraseñas no puedem tener más de 10 caracteres'

        elif contraseña2 != contraseña1:
            error_message = 'Las contraseñas no coinciden'

        elif cliente.emailExiste():
            error_message = 'El email ya tiene una cuenta'
        # guardar datos de cuenta
        if not error_message:
            cliente.contraseña1 = make_password(cliente.contraseña1)
            cliente.contraseña2 = make_password(cliente.contraseña2)
            cliente.save()
            if cliente:
                email = request.POST.get('email_cli')
                flag = check_password(contraseña1, cliente.contraseña1)
                if flag:
                    request.session['cuentaCliente'] = cliente.id_cliente
                    print('Eres', email)
                    return redirect('home')
                else:
                    error_message = 'Email o Contraseña Incorrecta'
            # messages.success(request, "Tu cuenta ha sido creada")
            # return redirect('login')
        else:
            data = {
                'values':value,
                'error': error_message,

            }
        return render(request, 'cliente/autoRegistroCliente.html',data)


def editar_perfil_cliente(request):
    check = Cliente.objects.filter(
        id_cliente=request.session['cuentaCliente'])
    if len(check) > 0:
        email = request.session['cuentaCliente']
        data = Cliente.objects.get(
            id_cliente=request.session['cuentaCliente'])
        data = {'cliente': data, 'email': email,'clienteeee':data}
    if request.method == 'POST':
        nombre_cli = request.POST["nombre_cli"]
        apaterno_cli = request.POST["apaterno_cli"]
        amaterno_cli = request.POST["amaterno_cli"]
        fono_cli = request.POST["fono_cli"]
        email_cli = request.POST["email_cli"]

        cliente = Cliente.objects.get(
            id_cliente=request.session['cuentaCliente'])
        cliente.nombre_cli = nombre_cli
        cliente.apaterno_cli = apaterno_cli
        cliente.amaterno_cli = amaterno_cli
        cliente.fono_cli = fono_cli
        cliente.email_cli = email_cli

        error_message = None
        if(not cliente.nombre_cli):
            error_message = 'El Nombre es requerido'
        elif not cliente.apaterno_cli:
            error_message = 'El Apellido es requerido'
        elif not cliente.amaterno_cli:
            error_message = 'El Apellido es requerido'
        elif len(cliente.fono_cli) > 9:
            error_message = 'El número no puede tener más de 9 digitos.'
        elif not cliente.email_cli:
            error_message = 'El email es requerido'

        # guardar datos de cuenta
        #corregir cuenta empleado y cliente
        if not error_message:
            if email_cli != cliente.email_cli:
                cliente.save()
                messages.success(request, "Email modificado, vuelva a iniciar sessión")
                return redirect('login')
            else:
                cliente.save()
                messages.success(request, "Datos modificados correctamente")
                return redirect('editar-perfil-cliente')
        else:
            email = request.session['cuentaCliente']
            data = {
                'email': email,
                'error': error_message,
                'clienteeee':check,
                'cliente':cliente
            }
    return render(request, 'cliente/editarPerfilCliente.html', data)

def cambiar_contraseña_cliente(request):
    check = Cliente.objects.filter(
        id_cliente=request.session['cuentaCliente'])
    if len(check) > 0:
        email = request.session['cuentaCliente']
        data = Cliente.objects.get(
            id_cliente=request.session['cuentaCliente'])
        data = {'data': data, 'email': email,'clienteeee':data}
    if request.method == "POST":
        contraseña_actual = request.POST['contraseña_actual']
        contraseña1 = request.POST['nueva_contraseña']
        contraseña2 = request.POST['con_nueva_contraseña']
        cuentaCliente = Cliente.get_cliente_by_id(email)
        if cuentaCliente:
            flag = check_password(contraseña_actual, cuentaCliente.contraseña1)
            error_message = None
            if flag:
                cliente = Cliente.objects.get(
                    id_cliente=request.session['cuentaCliente'])
                cliente.contraseña1 = contraseña1
                cliente.contraseña2 = contraseña2

                error_message = None
                if len(contraseña1 and contraseña2) < 5:
                    error_message = 'Las contraseñas deben tener mas de 5 caracteres'
                elif len(contraseña1 and contraseña2) > 10:
                    error_message = 'Las contraseñas no pueden tener más de 10 caracteres'
                elif contraseña2 != contraseña1:
                    error_message = 'Las contraseñas no coinciden'

                if not error_message:
                    cliente.contraseña1 = make_password(cliente.contraseña1)
                    cliente.contraseña2 = make_password(cliente.contraseña2)
                    cliente.save()
                    messages.success(
                        request, "Contraseña Cambiada Correctamente")
                    return redirect('cambiar-contraseña-cliente')
                else:
                    email = request.session['cuentaCliente']
                    data = {
                        'email': email,
                        'error': error_message,

                    }
                return render(request, 'cliente/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                email = request.session['cuentaCliente']
                data = {
                    'email': email,
                    'error': error_message,

                }
            return render(request, 'cliente/cambiar_contraseña.html', data)
    return render(request, "cliente/cambiar_contraseña.html", data)



class realizar_pedido(View):
    def get(self, request):
        #MODAL CARRITO
        clienteeee = Cliente.objects.get(id_cliente=request.session['cuentaCliente'])
        id_plato = (list(request.session.get('carro').keys()))
        platos_en_carro = Plato.get_plato_by_id_plato(id_plato)
        
        for plato in id_plato:
            platito = Plato.objects.get(id_plato=plato)
            print(platito.valor_plato)
        print(platos_en_carro)
        #FIN MODAL CARRITO
        platos = Plato.objects.all()
        tipo_pago = Pago.objects.all()
        data = {'platos':platos,'tipo_pago':tipo_pago,'platos_en_carro':platos_en_carro,'clienteeee':clienteeee}
        return render(request, 'cliente/realizarPedido.html',data)

    def post(self, request):
        direccion = request.POST.get('direccion')
        tipo_entrega = request.POST.get('tipo_entrega')
        tipo_pago = request.POST.get('tipo_pago')
        horario_entrega = request.POST.get('programar_horario_entrega')
        celular_contacto = request.POST.get('celular_contacto')
        cuentaCliente = request.session.get('cuentaCliente')
        carro = request.session.get('carro')
        platos = Plato.get_plato_by_id_plato(list(carro.keys()))
        print(direccion, tipo_entrega, tipo_pago, celular_contacto, cuentaCliente, carro,platos)

        print("tipo pago:")
        print(tipo_pago)
        if int(tipo_pago) == 3:
            print("entro a hacer el pago")
            id_cliente=cuentaCliente # obtenemos el rut de la persona a cobrar
            cliente = Cliente.objects.get(id_cliente=id_cliente) # obtenemos los datos del cliente de la base de datos

            costopedido = 0 # aca guaramos el costo a cobrar

            id_plato = (list(carro.keys()))
            for plato in id_plato:
                platito = Plato.objects.get(id_plato=plato)
                costopedido += platito.valor_plato


            saldonuevo = int(cliente.saldo_cli) - int(costopedido) # se resta la plata de la cuenta del cliente con el costo del pedido
            Cliente.objects.filter(id_cliente=id_cliente).update(saldo_cli=saldonuevo) # se actualiza el saldo del cliente


        for plato in platos:
            print(carro.get(str(plato.id_plato)))
            pedido = Pedido(cliente_id=Cliente(id_cliente=cuentaCliente),
                          plato_id=plato,
                          precio=plato.valor_plato,
                          horario_entrega=horario_entrega,
                          tipo_entrega=tipo_entrega,
                          tipo_pago_id=tipo_pago,
                          direccion=direccion,
                          celular=celular_contacto,
                          restaurant_id_restaurante=plato.Restaurant,
                          cantidad=carro.get(str(plato.id_plato)))
            pedido.pedido()
        request.session['carro'] = {}
        return redirect('mis-pedidos')


class pedidos(View):
    def get(self, request):
        clienteeee = Cliente.objects.get(id_cliente=request.session['cuentaCliente'])
        cuentaCliente = request.session.get('cuentaCliente')
        pedidos = Pedido.get_pedidos_by_cliente(cuentaCliente).filter(Q(estado="Pendiente")|Q(estado="Confirmado")|Q(estado="En ruta")).order_by("fecha_pedido")
        print(pedidos)
        data={'pedidos':pedidos,'clienteeee':clienteeee}
        return render(request, 'cliente/pedidos.html',data)

   

def descontar_saldo(request):

    id_cliente=request.session['cuentaCliente'] # obtenemos el rut de la persona a cobrar
    cliente = Cliente.objects.get(id_cliente=id_cliente) # obtenemos los datos del cliente de la base de datos

    costopedido = 0 # aca guaramos el costo a cobrar

    id_plato = (list(request.session.get('carro').keys()))
    for plato in id_plato:
        platito = Plato.objects.get(id_plato=plato)
        costopedido += platito.valor_plato


    saldonuevo = int(cliente.saldo_cli) - int(costopedido) # se resta la plata de la cuenta del cliente con el costo del pedido
    Cliente.objects.filter(id_cliente=id_cliente).update(saldo_cli=saldonuevo) # se actualiza el saldo del cliente
   #retorna a mis-pedidos
    return redirect('home')