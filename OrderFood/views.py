from django.contrib.messages.storage.base import Message
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django import views
from .models import *
from django.views import View
from django.contrib import messages
from .forms import ProveedorForm, PlatoForm
from .forms import ProveedorForm, PlatoForm, PedidoForm, GestionEmpresaForm
from .filters import buscarPlato


# Funciones Generales

def ubicacion(request):
    return render(request, 'ubicacion.html')

class home(View):
    def post(self,request):
        #PLATO ES EL NOMBRE QUE SE LE DA AL BOT
        plato = request.POST.get('plato')
        remove = request.POST.get('remove')
        carro = request.session.get('carro')
        if carro:
            quantity = carro.get(plato)
            if quantity:
                if remove:
                    if quantity <= 1:
                        carro.pop(plato)
                    else:
                        carro[plato] = quantity-1
                else:
                    carro[plato] = quantity+1
            else:
                carro[plato] = 1
        else:
            carro = {}
            carro[plato] = 1
        request.session['carro'] = carro
        print('carro',request.session['carro'])
        return redirect('home')

    def get(self, request):
        check = Cliente.objects.filter(
            id_cliente=request.session['cuentaCliente'])
        if len(check) > 0:
            clienteeee = Cliente.objects.get(
                id_cliente=request.session['cuentaCliente'])
        carro = request.session.get('carro')
        if not carro:
            request.session['carro'] = {}
        email = request.session.get('cuentaAdmin') or request.session.get(
        'cuentaEncConvenio') or request.session.get('cuentaEncCocina') or request.session.get('cuentaRepartidor') or request.session.get('cuentaCliente')
        platos = Plato.objects.all()
        rest = Restaurant.objects.all()
        buscar_plato = buscarPlato(request.GET, queryset=platos)
        platos = buscar_plato.qs
        #MODAL CARRITO
        id_plato = (list(request.session.get('carro').keys()))
        platos_en_carro = Plato.get_plato_by_id_plato(id_plato)
        print(platos_en_carro)
        #FIN MODAL CARRITO
        data = {'clienteeee':clienteeee,'email': email, 'platos': platos,
                'rest': rest, 'buscar_plato': buscar_plato,'platos_en_carro':platos_en_carro}
        return render(request, 'home.html', data)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        cuentaAdmin = Administrador.get_admin_by_email(email)
        cuentaEncCocina = EncCocina.get_enc_cocina_by_email(email)
        cuentaEncConvenio = EncConvenio.get_enc_convenio_by_email(email)
        cuentaRepartidor = Repartidor.get_repartidor_by_email(email)
        cuentaCliente = Cliente.get_cliente_by_email(email)
        error_message = None
        if cuentaAdmin:
            flag = check_password(contraseña, cuentaAdmin.contraseña1)
            if flag:
                request.session['cuentaAdmin'] = cuentaAdmin.email_admin
                print('eres: ', email)
                return redirect('home')
            else:
                error_message = 'Email o Contraseña incorrecto'
        elif cuentaEncCocina:
            flag = check_password(contraseña, cuentaEncCocina.contraseña1)
            if flag:
                request.session['cuentaEncCocina'] = cuentaEncCocina.email_enc_coc
                print('eres: ', email)
                return redirect('home')
            else:
                error_message = 'Email o Contraseña incorrecto'
        elif cuentaEncConvenio:
            flag = check_password(contraseña, cuentaEncConvenio.contraseña1)
            if flag:
                request.session['cuentaEncConvenio'] = cuentaEncConvenio.email_enc_conv
                print('eres :', email)
                return redirect('home')
            else:
                error_message = 'Email o Contraseña incorrecto'
        elif cuentaRepartidor:
            flag = check_password(contraseña, cuentaRepartidor.contraseña1)
            if flag:
                request.session['cuentaRepartidor'] = cuentaRepartidor.email_repartidor
                print('eres :', email)
                return redirect('home')
            else:
                error_message = 'Email o Contraseña incorrecto'
        elif cuentaCliente:
            flag = check_password(contraseña, cuentaCliente.contraseña1)
            if flag:
                request.session['cuentaCliente'] = cuentaCliente.id_cliente
                print('eres :',email)
                return redirect('home')
            else:
                error_message = 'Email o Contraseña incorrecto'
        return render(request, 'login.html', {'error': error_message})


class realizar_pedido(View):
    def get(self, request):
         #MODAL CARRITO
        id_plato = (list(request.session.get('carro').keys()))
        platos_en_carro = Plato.get_plato_by_id_plato(id_plato)
        print(platos_en_carro)
        #FIN MODAL CARRITO
        platos = Plato.objects.all()
        tipo_pago = Pago.objects.all()
        data = {'platos':platos,'tipo_pago':tipo_pago,'platos_en_carro':platos_en_carro}
        return render(request, 'realizarPedido.html',data)

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
                          cantidad=carro.get(str(plato.id_plato)))
            pedido.pedido()
            return redirect('mis-pedidos')





class pedidos(View):
    def get(self, request):
        cuentaCliente = request.session.get('cuentaCliente')
        pedidos = Pedido.get_pedidos_by_cliente(cuentaCliente)
        print(pedidos)
        return render(request, 'pedidos.html',{'pedidos':pedidos})


def logout(request):
    request.session.clear()
    return redirect('login')


# Modulo administracion
def editar_perfil_admin(request):
    check = Administrador.objects.filter(
        email_admin=request.session['cuentaAdmin'])
    if len(check) > 0:
        email = request.session['cuentaAdmin']
        data = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin'])
        data = {'data': data, 'email': email}
    if request.method == 'POST':
        nombre_adm = request.POST["nombre_adm"]
        apat_adm = request.POST["apat_adm"]
        amat_adm = request.POST["amat_adm"]
        email_admin = request.POST["email_admin"]
        fono_admin = request.POST["fono_admin"]

        admin = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin'])
        admin.nombre_adm = nombre_adm
        admin.apat_adm = apat_adm
        admin.amat_adm = amat_adm
        admin.email_admin = email_admin
        admin.fono_admin = fono_admin

        error_message = None
        if(not admin.nombre_adm):
            error_message = 'El nombre es requerido'
        elif not admin.apat_adm:
            error_message = 'El Apellido Paterno es requerido'
        elif not admin.amat_adm:
            error_message = 'El Apellido Materno es requerido'
        elif not admin.fono_admin:
            error_message = 'El Fono requerido'
        elif len(admin.fono_admin) > 9:
            error_message = 'El fono no puede tener mas de 9 digitos'

        # guardar datos de cuenta
        if not error_message:
            admin.save()
            messages.success(request, "Datos editados correctamente")
            return redirect('editar-perfil')
        else:
            email = request.session['cuentaAdmin']
            data = {
                'email': email,
                'error': error_message,
            }
    return render(request, 'administrador/editarPerfil.html', data)


def cambiar_contraseña_admin(request):
    check = Administrador.objects.filter(
        email_admin=request.session['cuentaAdmin'])
    if len(check) > 0:
        email = request.session['cuentaAdmin']
        data = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin'])
        data = {'data': data, 'email': email}
    if request.method == "POST":
        contraseña_actual = request.POST['contraseña_actual']
        contraseña1 = request.POST['nueva_contraseña']
        contraseña2 = request.POST['con_nueva_contraseña']
        cuentaAdmin = Administrador.get_admin_by_email(email)
        if cuentaAdmin:
            flag = check_password(contraseña_actual, cuentaAdmin.contraseña1)
            error_message = None
            if flag:
                admin = Administrador.objects.get(
                    email_admin=request.session['cuentaAdmin'])
                admin.contraseña1 = contraseña1
                admin.contraseña2 = contraseña2

                error_message = None
                if len(contraseña1 and contraseña2) < 5:
                    error_message = 'Las contraseñas deben tener mas de 5 caracteres'
                elif len(contraseña1 and contraseña2) > 10:
                    error_message = 'Las contraseñas no pueden tener más de 10 caracteres'
                elif contraseña2 != contraseña1:
                    error_message = 'Las contraseñas no coinciden'

                if not error_message:
                    admin.contraseña1 = make_password(admin.contraseña1)
                    admin.contraseña2 = make_password(admin.contraseña2)
                    admin.save()
                    messages.success(
                        request, "Contraseña Cambiada Correctamente")
                    return redirect('cambiar-contraseña')
                else:
                    email = request.session['cuentaAdmin']
                    data = {
                        'email': email,
                        'error': error_message,

                    }
                return render(request, 'administrador/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                email = request.session['cuentaAdmin']
                data = {
                    'email': email,
                    'error': error_message,

                }
            return render(request, 'administrador/cambiar_contraseña.html', data)
    return render(request, "administrador/cambiar_contraseña.html", data)


def generar_cuenta_enc_cocina(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        email = request.session['cuentaAdmin']
        cuentasEncCocina = EncCocina.objects.all()
        data = {
            'email': email,
            'cuentasEncCocina': cuentasEncCocina
        }
        return render(request, 'administrador/cuenta/encargadoCocina/gestionarEncCocina.html', data)
    else:
        postData = request.POST
        nom_enc_coc = postData.get('nom_enc_coc')
        titulo = postData.get('titulo')
        exp_laboral = postData.get('exp_laboral')
        celular = postData.get('celular')
        email_enc_coc = postData.get('email_enc_coc')
        contraseña1 = postData.get('contraseña1')
        contraseña2 = postData.get('contraseña2')
        # validaciones
        value = {
            'nom_enc_coc': nom_enc_coc,
            'titulo': titulo,
            'exp_laboral': exp_laboral,
            'celular': celular,
            'email_enc_coc': email_enc_coc,
        }
        error_message = None
        encCocina = EncCocina(nom_enc_coc=nom_enc_coc,
                              titulo=titulo,
                              exp_laboral=exp_laboral,
                              celular=celular,
                              email_enc_coc=email_enc_coc,
                              contraseña1=contraseña1,
                              contraseña2=contraseña2)
        if(not nom_enc_coc):
            error_message = 'El nombre es requerido'
        elif len(nom_enc_coc) < 4:
            error_message = 'El nombre debe tener mas de 4 caracteres'

        elif not titulo:
            error_message = 'El titulo es requerido'
        elif len(titulo) < 4:
            error_message = 'El titulo debe tener mas de 4 caracteres'

        elif not exp_laboral:
            error_message = 'La experiencia laboral es requerida'
        elif len(exp_laboral) < 0:
            error_message = 'La experiencia laboral debe ser mayor a 0'

        elif not email_enc_coc:
            error_message = 'El email es requerido'

        elif not celular:
            error_message = 'EL celular es requierodo'
        elif len(celular) < 7:
            error_message = 'El celular debe tener mas de 7 digitos'

        elif len(contraseña1 and contraseña2) < 5:
            error_message = 'Las contraseñas deben tener mas de 5 caracteres'

        elif contraseña2 != contraseña1:
            error_message = 'Las contraseñas no coinciden'

        elif encCocina.siExiste():
            error_message = 'El email ya tiene una cuenta'

        # guadar datos de cuenta
        if not error_message:
            encCocina.contraseña1 = make_password(encCocina.contraseña1)
            encCocina.contraseña2 = make_password(encCocina.contraseña2)
            encCocina.cuentaEncargadoCocina()
            messages.success(request, "Cuenta Encargado Cocina Generada")
            return redirect('gestionar-encCocina')
        else:
            email = request.session['cuentaAdmin']
            cuentasEncCocina = EncCocina.objects.all()
            data = {
                'email': email,
                'cuentasEncCocina': cuentasEncCocina,
                'error': error_message,
                'values': value,
            }
        return render(request, 'administrador/cuenta/encargadoCocina/gestionarEncCocina.html', data)


def editar_cuenta_enc_cocina(request):
    email = request.session['cuentaAdmin']
    id_enc_coc = request.GET["id_enc_coc"]
    cuentaEncCocina = get_object_or_404(EncCocina, id_enc_coc=id_enc_coc)
    data1 = {
        'email': email,
        'cuentaEncCocina': cuentaEncCocina
    }

    if request.method == "POST":
        nom_enc_coc = request.POST["nom_enc_coc"]
        titulo = request.POST["titulo"]
        exp_laboral = request.POST["exp_laboral"]
        celular = request.POST["celular"]
        email_enc_coc = request.POST["email_enc_coc"]

        cuentaEncCocina.nom_enc_coc = nom_enc_coc
        cuentaEncCocina.titulo = titulo
        cuentaEncCocina.exp_laboral = exp_laboral
        cuentaEncCocina.celular = celular
        cuentaEncCocina.email_enc_coc = email_enc_coc

        error_message = None
        if(not cuentaEncCocina.nom_enc_coc):
            error_message = 'El nombre es requerido'
        elif len(cuentaEncCocina.nom_enc_coc) < 4:
            error_message = 'El nombre debe tener mas de 4 caracteres'

        elif not cuentaEncCocina.titulo:
            error_message = 'El titulo es requerido'
        elif len(cuentaEncCocina.titulo) < 4:
            error_message = 'El titulo debe tener mas de 4 caracteres'
        elif not cuentaEncCocina.exp_laboral:
            error_message = 'La experiencia laboral es requerida'
        elif len(cuentaEncCocina.exp_laboral) < 0:
            error_message = 'La experiencia laboral debe ser mayor a 0'

        elif not cuentaEncCocina.celular:
            error_message = 'EL celular es requierodo'
        elif len(cuentaEncCocina.celular) < 7:
            error_message = 'El celular debe tener mas de 7 digitos'
        elif len(cuentaEncCocina.celular) > 9:
            error_message = 'El celular no puede tener mas de 9 digitos'

        # guardar datos de cuenta
        if not error_message:
            cuentaEncCocina.save()
            messages.success(request, "Cuenta Encargado Cocina Editada")
            return redirect('gestionar-encCocina')
        else:
            email = request.session['cuentaAdmin']
            cuentasEncCocina = EncCocina.objects.all()
            data = {
                'email': email,
                'cuentasEncCocina': cuentasEncCocina,
                'error': error_message,
                'cuentaEncCocina': cuentaEncCocina
            }
        return render(request, 'administrador/cuenta/encargadoCocina/edicionEncCocina.html', data)
    return render(request, 'administrador/cuenta/encargadoCocina/edicionEncCocina.html', data1)


def eliminar_cuenta_enc_cocina(request):
    id_enc_coc = request.GET["id_enc_coc"]
    cuentasEncCocina = EncCocina.objects.get(id_enc_coc=id_enc_coc)
    cuentasEncCocina.delete()
    return redirect('gestionar-encCocina')


def generar_cuenta_enc_convenio(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        email = request.session['cuentaAdmin']
        cuentasEncConvenio = EncConvenio.objects.all()
        data = {
            'cuentasEncConvenio': cuentasEncConvenio,
            'email': email
        }
        return render(request, 'administrador/cuenta/encargadoConvenio/gestionarEncConvenio.html', data)
    else:
        postData = request.POST
        rut_enc_conv = postData.get('rut_enc_conv')
        nom_enc_conv = postData.get('nom_enc_conv')
        ap_enc_conv = postData.get('ap_enc_conv')
        email_enc_conv = postData.get('email_enc_conv')
        celular = postData.get('celular')
        contraseña1 = postData.get('contraseña1')
        contraseña2 = postData.get('contraseña2')

        # validaciones
        value = {
            'rut_enc_conv': rut_enc_conv,
            'nom_enc_conv': nom_enc_conv,
            'ap_enc_conv': ap_enc_conv,
            'email_enc_conv': email_enc_conv,
            'celular': celular,
        }
        error_message = None
        encConvenio = EncConvenio(rut_enc_conv=rut_enc_conv,
                                  nom_enc_conv=nom_enc_conv,
                                  ap_enc_conv=ap_enc_conv,
                                  email_enc_conv=email_enc_conv,
                                  celular=celular,
                                  contraseña1=contraseña1,
                                  contraseña2=contraseña2)
        if(not rut_enc_conv):
            error_message = 'El Rut es requerido'
        elif len(rut_enc_conv) < 8:
            error_message = 'El Rut debe tener mas de 8 digitos'
        elif len(rut_enc_conv) > 12:
            error_message = 'El Rut no debe tener mas de 12 digitos'

        elif not nom_enc_conv:
            error_message = 'El Nombre es requerido'
        elif len(nom_enc_conv) < 4:
            error_message = 'El Nombre debe tener mas de 4 caracteres'

        elif not ap_enc_conv:
            error_message = 'El Apellido  es requerida'
        elif len(ap_enc_conv) < 2:
            error_message = 'EL appelido debe tener mas de 2'

        elif not email_enc_conv:
            error_message = 'El email es requerido'

        elif not celular:
            error_message = 'EL celular es requierodo'
        elif len(celular) < 7:
            error_message = 'El celular debe tener mas de 7 digitos'

        elif len(contraseña1 and contraseña2) < 5:
            error_message = 'Las contraseñas deben tener mas de 5 caracteres'

        elif len(contraseña1 and contraseña2) > 10:
            error_message = 'Las contraseñas no puede ser mayor a 10 caracteres'

        elif contraseña2 != contraseña1:
            error_message = 'Las contraseñas no coinciden'

        elif encConvenio.emailExiste():
            error_message = 'El email ya tiene una cuenta'

        elif encConvenio.rutExiste():
            error_message = 'El Rut ya tiene una cuenta'

        # guardar datos de cuenta
        if not error_message:
            encConvenio.contraseña1 = make_password(encConvenio.contraseña1)
            encConvenio.contraseña2 = make_password(encConvenio.contraseña2)
            encConvenio.cuentaEncargadoConvenio()
            messages.success(request, "Cuenta Encargado Convenio Generada")
            return redirect('gestionar-enc-convenio')
        else:
            email = request.session['cuentaAdmin']
            cuentasEncConvenio = EncConvenio.objects.all()
            data = {
                'email': email,
                'cuentasEncConvenio': cuentasEncConvenio,
                'error': error_message,
                'values': value,
            }
        return render(request, 'administrador/cuenta/encargadoConvenio/gestionarEncConvenio.html', data)


def editar_cuenta_enc_convenio(request):
    email = request.session['cuentaAdmin']
    id_enc_conv = request.GET["id_enc_conv"]
    cuentaEncConvenio = get_object_or_404(EncConvenio, id_enc_conv=id_enc_conv)
    data1 = {
        'email': email,
        'cuentaEncConvenio': cuentaEncConvenio
    }

    if request.method == "POST":
        rut_enc_conv = request.POST['rut_enc_conv']
        nom_enc_conv = request.POST['nom_enc_conv']
        ap_enc_conv = request.POST['ap_enc_conv']
        email_enc_conv = request.POST['email_enc_conv']
        celular = request.POST['celular']

        cuentaEncConvenio.rut_enc_conv = rut_enc_conv
        cuentaEncConvenio.nom_enc_conv = nom_enc_conv
        cuentaEncConvenio.ap_enc_conv = ap_enc_conv
        cuentaEncConvenio.email_enc_conv = email_enc_conv
        cuentaEncConvenio.celular = celular

        error_message = None
        if(not cuentaEncConvenio.rut_enc_conv):
            error_message = 'El Rut es requerido'
        elif len(cuentaEncConvenio.rut_enc_conv) < 8:
            error_message = 'El Rut debe tener mas de 8 digitos'
        elif len(cuentaEncConvenio.rut_enc_conv) > 12:
            error_message = 'El Rut no debe tener mas de 12 digitos'

        elif not cuentaEncConvenio.nom_enc_conv:
            error_message = 'El Nombre es requerido'
        elif len(cuentaEncConvenio.nom_enc_conv) < 4:
            error_message = 'El Nombre debe tener mas de 4 caracteres'

        elif not cuentaEncConvenio.ap_enc_conv:
            error_message = 'El Apellido  es requerida'
        elif len(cuentaEncConvenio.ap_enc_conv) < 2:
            error_message = 'EL appelido debe tener mas de 2'

        elif not cuentaEncConvenio.email_enc_conv:
            error_message = 'El email es requerido'

        elif not cuentaEncConvenio.celular:
            error_message = 'EL celular es requierodo'
        elif len(cuentaEncConvenio.celular) < 7:
            error_message = 'El celular debe tener mas de 7 digitos'
        elif len(cuentaEncConvenio.celular) > 9:
            error_message = 'El celular no debe tener mas de 9 digitos'

        # guardar datos de cuenta
        if not error_message:
            cuentaEncConvenio.save()
            messages.success(request, "Cuenta Encargado Convenio Editada")
            return redirect('gestionar-enc-convenio')
        else:
            email = request.session['cuentaAdmin']
            cuentasEncConvenio = EncConvenio.objects.all()
            data = {
                'email': email,
                'error': error_message,
                'cuentasEncConvenio': cuentasEncConvenio,
                'cuentaEncConvenio': cuentaEncConvenio
            }
        return render(request, 'administrador/cuenta/encargadoConvenio/edicionEncConvenio.html', data)
    return render(request, 'administrador/cuenta/encargadoConvenio/edicionEncConvenio.html', data1)



def eliminar_cuenta_enc_convenio(request):
    id_enc_conv = request.GET["id_enc_conv"]
    cuentaEncConvenio = EncConvenio.objects.get(id_enc_conv=id_enc_conv)
    cuentaEncConvenio.delete()
    return redirect('gestionar-enc-convenio')


def generar_cuenta_repartidor(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        email = request.session['cuentaAdmin']
        cuentasRepartidor = Repartidor.objects.all()
        data = {
            'cuentasRepartidor': cuentasRepartidor,
            'email': email
        }
        return render(request, 'administrador/cuenta/repartidor/gestionarRepartidor.html', data)
    else:
        postData = request.POST
        rut_repartidor = postData.get('rut_repartidor')
        nombre_repartidor = postData.get('nombre_repartidor')
        apellido_repartidor = postData.get('apellido_repartidor')
        email_repartidor = postData.get('email_repartidor')
        tipo_veh = postData.get('tipo_veh')
        patente_veh_moto = postData.get('patente_veh_moto')
        patente_veh_auto = postData.get('patente_veh_auto')
        celular = postData.get('celular')
        contraseña1 = postData.get('contraseña1')
        contraseña2 = postData.get('contraseña2')

        # validaciones
        value = {
            'rut_repartidor': rut_repartidor,
            'nombre_repartidor': nombre_repartidor,
            'apellido_repartidor': apellido_repartidor,
            'email_repartidor': email_repartidor,
            'tipo_veh': tipo_veh,
            'patente_veh': (patente_veh_moto or patente_veh_auto),
            'celular': celular,
        }
        error_message = None
        repartidor = Repartidor(rut_repartidor=rut_repartidor,
                                nombre_repartidor=nombre_repartidor,
                                apellido_repartidor=apellido_repartidor,
                                email_repartidor=email_repartidor,
                                tipo_veh=tipo_veh,
                                patente_veh=(
                                    patente_veh_auto or patente_veh_moto),
                                celular=celular,
                                contraseña1=contraseña1,
                                contraseña2=contraseña2)
        if(not rut_repartidor):
            error_message = 'El Rut es requerido'
        elif len(rut_repartidor) < 8:
            error_message = 'El Rut debe tener mas de 8 digitos'
        elif len(rut_repartidor) > 12:
            error_message = 'El Rut no debe tener mas de 12 digitos'

        elif not nombre_repartidor:
            error_message = 'El Nombre es requerido'
        elif len(nombre_repartidor) < 4:
            error_message = 'El Nombre debe tener mas de 4 caracteres'

        elif not apellido_repartidor:
            error_message = 'El Apellido  es requerida'
        elif len(apellido_repartidor) < 2:
            error_message = 'EL appelido debe tener mas de 2'

        elif not email_repartidor:
            error_message = 'El email es requerido'

        elif not tipo_veh:
            error_message = 'Tipo de vehiculo requerido'

        elif not celular:
            error_message = 'EL celular es requierodo'
        elif len(celular) < 7:
            error_message = 'El celular debe tener mas de 7 digitos'

        elif len(contraseña1 and contraseña2) < 5:
            error_message = 'Las contraseñas deben tener mas de 5 caracteres'

        elif len(contraseña1 and contraseña2) > 10:
            error_message = 'Las contraseñas no puedem tener más de 10 caracteres'

        elif contraseña2 != contraseña1:
            error_message = 'Las contraseñas no coinciden'

        elif repartidor.emailExiste():
            error_message = 'El email ya tiene una cuenta'

        elif repartidor.rutExiste():
            error_message = 'El Rut ya tiene una cuenta'

        elif repartidor.patenteExiste():
            error_message = 'La patente ya esta registrada'

        # guardar datos de cuenta
        if not error_message:
            repartidor.contraseña1 = make_password(repartidor.contraseña1)
            repartidor.contraseña2 = make_password(repartidor.contraseña2)
            repartidor.cuentaRepartidor()
            messages.success(request, "Cuenta Repartidor Generada")
            return redirect('gestionar-repartidor')
        else:
            email = request.session['cuentaAdmin']
            cuentasRepartidor = Repartidor.objects.all()
            data = {
                'email': email,
                'cuentasRepartidor': cuentasRepartidor,
                'error': error_message,
                'values': value
            }
        return render(request, 'administrador/cuenta/repartidor/gestionarRepartidor.html', data)


def editar_cuenta_repartidor(request):
    email = request.session['cuentaAdmin']
    id_repartidor = request.GET["id_repartidor"]
    cuentaRepartidor = get_object_or_404(
        Repartidor, id_repartidor=id_repartidor)
    data1 = {
        'email': email,
        'cuentaRepartidor': cuentaRepartidor
    }
    if request.method == "POST":
        rut_repartidor = request.POST['rut_repartidor']
        nombre_repartidor = request.POST['nombre_repartidor']
        apellido_repartidor = request.POST['apellido_repartidor']
        email_repartidor = request.POST['email_repartidor']
        tipo_veh = request.POST['tipo_veh']
        patente_veh_moto = request.POST['patente_veh_moto']
        patente_veh_auto = request.POST['patente_veh_auto']
        celular = request.POST['celular']

        cuentaRepartidor.rut_repartidor = rut_repartidor
        cuentaRepartidor.nombre_repartidor = nombre_repartidor
        cuentaRepartidor.apellido_repartidor = apellido_repartidor
        cuentaRepartidor.email_repartidor = email_repartidor
        cuentaRepartidor.tipo_veh = tipo_veh
        cuentaRepartidor.patente_veh = (patente_veh_moto or patente_veh_auto)
        cuentaRepartidor.celular = celular

        error_message = None
        if(not cuentaRepartidor.rut_repartidor):
            error_message = 'El Rut es requerido'
        elif len(cuentaRepartidor.rut_repartidor) < 8:
            error_message = 'El Rut debe tener mas de 8 digitos'
        elif len(cuentaRepartidor.rut_repartidor) > 12:
            error_message = 'El Rut no debe tener mas de 12 digitos'

        elif not cuentaRepartidor.nombre_repartidor:
            error_message = 'El Nombre es requerido'
        elif len(cuentaRepartidor.nombre_repartidor) < 4:
            error_message = 'El Nombre debe tener mas de 4 caracteres'

        elif not cuentaRepartidor.apellido_repartidor:
            error_message = 'El Apellido  es requerida'
        elif len(cuentaRepartidor.apellido_repartidor) < 2:
            error_message = 'EL appelido debe tener mas de 2'

        elif not cuentaRepartidor.email_repartidor:
            error_message = 'El email es requerido'

        elif not cuentaRepartidor.tipo_veh:
            error_message = 'Tipo de vehiculo requerido'

        elif not cuentaRepartidor.celular:
            error_message = 'EL celular es requierodo'
        elif len(cuentaRepartidor.celular) < 7:
            error_message = 'El celular debe tener mas de 7 digitos'
        elif len(cuentaRepartidor.celular) > 9:
            error_message = 'El celular no puede tener mas de 9 digitos'

        # guardar datos de cuenta
        if not error_message:
            cuentaRepartidor.save()
            messages.success(request, "Cuenta Repartidor Editada")
            return redirect('gestionar-repartidor')
        else:
            email = request.session['cuentaAdmin']
            cuentasRepartidor = Repartidor.objects.all()
            data = {
                'email': email,
                'error': error_message,
                'cuentasRepartidor': cuentasRepartidor,
                'cuentaRepartidor': cuentaRepartidor
            }
        return render(request, 'administrador/cuenta/repartidor/edicionRepartidor.html', data)
    return render(request, 'administrador/cuenta/repartidor/edicionRepartidor.html', data1)


def eliminar_cuenta_repartidor(request):
    id_repartidor = request.GET["id_repartidor"]
    cuentaRepartidor = get_object_or_404(
        Repartidor, id_repartidor=id_repartidor)
    cuentaRepartidor.delete()
    return redirect('gestionar-repartidor')


# Fin modulo administracion


# Modulo repartidor
def editar_perfil_repartidor(request):
    check = Repartidor.objects.filter(
        email_repartidor=request.session['cuentaRepartidor'])
    if len(check) > 0:
        email = request.session['cuentaRepartidor']
        data = Repartidor.objects.get(
            email_repartidor=request.session['cuentaRepartidor'])
        data = {'data': data, 'email': email}
    if request.method == 'POST':
        rut_repartidor = request.POST["rut_repartidor"]
        nombre_repartidor = request.POST["nombre_repartidor"]
        apellido_repartidor = request.POST["apellido_repartidor"]
        email_repartidor = request.POST["email_repartidor"]
        tipo_veh = request.POST["tipo_veh"]
        celular = request.POST["celular"]

        repartidor = Repartidor.objects.get(
            email_repartidor=request.session['cuentaRepartidor'])
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
            email = request.session['cuentaRepartidor']
            data = {
                'email': email,
                'error': error_message,
            }
    return render(request, 'repartidor/editarPerfil.html', data)


def cambiar_contraseña_repartidor(request):
    check = Repartidor.objects.filter(
        email_repartidor=request.session['cuentaRepartidor'])
    if len(check) > 0:
        email = request.session['cuentaRepartidor']
        data = Repartidor.objects.get(
            email_repartidor=request.session['cuentaRepartidor'])
        data = {'data': data, 'email': email}
    if request.method == "POST":
        contraseña_actual = request.POST['contraseña_actual']
        contraseña1 = request.POST['nueva_contraseña']
        contraseña2 = request.POST['con_nueva_contraseña']
        cuentaRepartidor = Repartidor.get_repartidor_by_email(email)
        if cuentaRepartidor:
            flag = check_password(
                contraseña_actual, cuentaRepartidor.contraseña1)
            error_message = None
            if flag:
                repartidor = Repartidor.objects.get(
                    email_repartidor=request.session['cuentaRepartidor'])
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
                    email = request.session['cuentaRepartidor']
                    data = {
                        'email': email,
                        'error': error_message,

                    }
                return render(request, 'repartidor/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                email = request.session['cuentaRepartidor']
                data = {
                    'email': email,
                    'error': error_message,

                }
            return render(request, 'repartidor/cambiar_contraseña.html', data)
    return render(request, "repartidor/cambiar_contraseña.html", data)

# Fin Modulo repartidor


# Modulo Encargado Cocina
def editar_perfil_enc_cocina(request):
    check = EncCocina.objects.filter(
        email_enc_coc=request.session['cuentaEncCocina'])
    if len(check) > 0:
        email = request.session['cuentaEncCocina']
        data = EncCocina.objects.get(
            email_enc_coc=request.session['cuentaEncCocina'])
        data = {'data': data, 'email': email}
    if request.method == 'POST':
        nom_enc_coc = request.POST["nom_enc_coc"]
        titulo = request.POST["titulo"]
        exp_laboral = request.POST["exp_laboral"]
        email_enc_coc = request.POST["email_enc_coc"]
        celular = request.POST["celular"]

        encCocina = EncCocina.objects.get(
            email_enc_coc=request.session['cuentaEncCocina'])
        encCocina.nom_enc_coc = nom_enc_coc
        encCocina.titulo = titulo
        encCocina.exp_laboral = exp_laboral
        encCocina.email_enc_coc = email_enc_coc
        encCocina.celular = celular

        error_message = None
        if(not encCocina.nom_enc_coc):
            error_message = 'El nombre es requerido'
        elif not encCocina.titulo:
            error_message = 'El Titulo es requerido'
        elif not encCocina.exp_laboral:
            error_message = 'La experiencia laboral es requerida'
        elif not encCocina.email_enc_coc:
            error_message = 'El Email es requerido'
        elif not encCocina.celular:
            error_message = 'El celular es requerido'
        elif len(encCocina.celular) > 9:
            error_message = 'El Celular no puede tener mas de 9 digitos'

        # guardar datos de cuenta
        if not error_message:
            encCocina.save()
            messages.success(request, "Datos editados correctamente")
            return redirect('editar-perfil-enc-cocina')
        else:
            email = request.session['cuentaEncCocina']
            data = {
                'email': email,
                'error': error_message,
            }
    return render(request, 'encargadoCocina/editarPerfil.html', data)


def cambiar_contraseña_enc_cocina(request):
    check = EncCocina.objects.filter(
        email_enc_coc=request.session['cuentaEncCocina'])
    if len(check) > 0:
        email = request.session['cuentaEncCocina']
        data = EncCocina.objects.get(
            email_enc_coc=request.session['cuentaEncCocina'])
        data = {'data': data, 'email': email}
    if request.method == "POST":
        contraseña_actual_cocina = request.POST['contraseña_actual_cocina']
        contraseña1 = request.POST['nueva_contraseña_cocina']
        contraseña2 = request.POST['con_nueva_contraseña_cocina']
        cuentaEncCocina = EncCocina.get_enc_cocina_by_email(email)
        if cuentaEncCocina:
            flag = check_password(contraseña_actual_cocina,
                                  cuentaEncCocina.contraseña1)
            error_message = None
            if flag:
                enCocina = EncCocina.objects.get(
                    email_enc_coc=request.session['cuentaEncCocina'])
                enCocina.contraseña1 = contraseña1
                enCocina.contraseña2 = contraseña2

                error_message = None
                if len(contraseña1 and contraseña2) < 5:
                    error_message = 'Las contraseñas deben tener mas de 5 caracteres'
                elif len(contraseña1 and contraseña2) > 10:
                    error_message = 'Las contraseñas no pueden tener más de 10 caracteres'
                elif contraseña2 != contraseña1:
                    error_message = 'Las contraseñas no coinciden'

                if not error_message:
                    enCocina.contraseña1 = make_password(enCocina.contraseña1)
                    enCocina.contraseña2 = make_password(enCocina.contraseña2)
                    enCocina.cuentaEncargadoCocina()
                    messages.success(
                        request, "Contraseña Cambiada Correctamente")
                    return redirect('cambiar-contraseña-enc-cocina')
                else:
                    email = request.session['cuentaEncCocina']
                    data = {
                        'email': email,
                        'error': error_message,

                    }
                return render(request, 'encargadoCocina/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                email = request.session['cuentaEncCocina']
                data = {
                    'email': email,
                    'error': error_message,

                }
            return render(request, 'encargadoCocina/cambiar_contraseña.html', data)
    return render(request, "encargadoCocina/cambiar_contraseña.html", data)


def gestionar_plato(request):
    request.session.set_expiry(10000)
    email = request.session['cuentaEncCocina']
    plato = Plato.objects.all()
    data = {
        'email': email,
        'plato': plato,
        'form': PlatoForm()
    }

    if request.method == 'POST':
        formulario = PlatoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Plato Agregado Correctamente")
            return redirect(to="gestionar-plato")
        else:
            data["form"] = formulario

    return render(request, 'encargadoCocina/menu/gestionarPlato.html', data)


def modificar_plato(request):
    email = request.session['cuentaEncCocina']
    id_plato = request.GET["id_plato"]
    plato = get_object_or_404(Plato, id_plato=id_plato)

    data = {
        'email': email,
        'form': PlatoForm(instance=plato)
    }
    if request.method == 'POST':
        formulario = PlatoForm(
            data=request.POST, instance=plato, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Plato Modificado Correctamente")
            return redirect(to="gestionar-plato")
        else:
            data["form"] = formulario

    return render(request, 'encargadoCocina/menu/modificar.html', data)


def eliminar_plato(request):
    id_plato = request.GET["id_plato"]
    plato = get_object_or_404(Plato, id_plato=id_plato)
    plato.delete()
    messages.success(request, "Plato Eliminado Correctamente")
    return redirect(to="gestionar-plato")


# contacto proveedor que realiza una oferta la vera el encargado cocina en su modulo
def proveedor(request):
    data = {
        'form': ProveedorForm()
    }
    if request.method == 'POST':
        formulario = ProveedorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Hemos recibido tu oferta, pronto nos contactaremos contigo")
        else:
            data["form"] = formulario

    return render(request, 'encargadoCocina/proveedor/contactoProveedor.html', data)


def listar_proveedor(request):
    request.session.set_expiry(10000)
    email = request.session['cuentaEncCocina']
    proveedores = Proveedor.objects.all()
    data = {
        'proveedores': proveedores,
        'email': email
    }
    return render(request, 'encargadoCocina/proveedor/listar.html', data)


def modificar_proveedor(request):
    request.session.set_expiry(10000)
    email = request.session['cuentaEncCocina']
    id_proveedor = request.GET["id_proveedor"]
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)

    data = {
        'form': ProveedorForm(instance=proveedor),
        'email': email
    }

    if request.method == 'POST':
        formulario = ProveedorForm(data=request.POST, instance=proveedor)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificación exitosa")
            return redirect(to="listar_proveedor")
        data["form"] = formulario

    return render(request, 'encargadoCocina/proveedor/modificar.html', data)


def eliminar_proveedor(request):
    id_proveedor = request.GET["id_proveedor"]
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    proveedor.delete()
    messages.success(request, "Eliminación exitosa")
    return redirect(to="listar_proveedor")


# Fin modulo encargado Cocina


# pedidos
def agregar_pedido(request):

    data = {
        'form': PedidoForm()
    }
    if request.method == 'POST':
        formulario = PedidoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado correctamente"
        else:
            data["form"] = formulario

    return render(request, 'pedido/agregar.html', data)


def listar_pedido(request):
    pedidos = Pedido.objects.all()
    data = {
        'pedidos': pedidos
    }

    return render(request, 'pedido/listar.html', data)


def modificar_pedido(request, id):

    pedido = get_object_or_404(Pedido, id_pedido=id)

    data = {
        'form': PedidoForm(instance=pedido)
    }

    if request.method == 'POST':
        formulario = PedidoForm(data=request.POST, instance=pedido)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_pedido")
        data["form"] = formulario

    return render(request, 'pedido/modificar.html', data)


def eliminar_pedido(request, id):

    pedido = get_object_or_404(Pedido, id_pedido=id)
    pedido.delete()
    return redirect(to="listar_pedido")

# fin pedido


# Modulo Encargado Convenio
def editar_perfil_enc_convenio(request):
    check = EncConvenio.objects.filter(
        email_enc_conv=request.session['cuentaEncConvenio'])
    if len(check) > 0:
        email = request.session['cuentaEncConvenio']
        data = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
        data = {'data': data, 'email': email}
    if request.method == 'POST':
        rut_enc_conv = request.POST["rut_enc_conv"]
        nom_enc_conv = request.POST["nom_enc_conv"]
        ap_enc_conv = request.POST["ap_enc_conv"]
        email_enc_conv = request.POST["email_enc_conv"]
        celular = request.POST["celular"]

        encConvenio = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
        encConvenio.rut_enc_conv = rut_enc_conv
        encConvenio.nom_enc_conv = nom_enc_conv
        encConvenio.ap_enc_conv = ap_enc_conv
        encConvenio.email_enc_conv = email_enc_conv
        encConvenio.celular = celular

        error_message = None
        if(not encConvenio.rut_enc_conv):
            error_message = 'El Rut es requerido'
        elif not encConvenio.nom_enc_conv:
            error_message = 'El Nombre es requerido'
        elif not encConvenio.ap_enc_conv:
            error_message = 'El Apellido es requerido'
        elif not encConvenio.email_enc_conv:
            error_message = 'El Email es requerido'
        elif not encConvenio.celular:
            error_message = 'El celular es requerido'
        elif len(encConvenio.celular) > 9:
            error_message = 'El Celular no puede tener mas de 9 digitos'

        # guardar datos de cuenta
        if not error_message:
            encConvenio.save()
            messages.success(request, "Datos editados correctamente")
            return redirect('editar-perfil-enc-convenio')
        else:
            email = request.session['cuentaEncConvenio']
            data = {
                'email': email,
                'error': error_message,
            }
    return render(request, 'encargadoConvenio/editarPerfil.html', data)


def cambiar_contraseña_enc_convenio(request):
    check = EncConvenio.objects.filter(
        email_enc_conv=request.session['cuentaEncConvenio'])
    if len(check) > 0:
        email = request.session['cuentaEncConvenio']
        data = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
        data = {'data': data, 'email': email}
    if request.method == "POST":
        contraseña_actual = request.POST['contraseña_actual']
        contraseña1 = request.POST['nueva_contraseña']
        contraseña2 = request.POST['con_nueva_contraseña']
        cuentaEncConvenio = EncConvenio.get_enc_convenio_by_email(email)
        if cuentaEncConvenio:
            flag = check_password(
                contraseña_actual, cuentaEncConvenio.contraseña1)
            error_message = None
            if flag:
                enConvenio = EncConvenio.objects.get(
                    email_enc_conv=request.session['cuentaEncConvenio'])
                enConvenio.contraseña1 = contraseña1
                enConvenio.contraseña2 = contraseña2

                error_message = None
                if len(contraseña1 and contraseña2) < 5:
                    error_message = 'Las contraseñas deben tener mas de 5 caracteres'
                elif len(contraseña1 and contraseña2) > 10:
                    error_message = 'Las contraseñas no pueden tener más de 10 caracteres'
                elif contraseña2 != contraseña1:
                    error_message = 'Las contraseñas no coinciden'

                if not error_message:
                    enConvenio.contraseña1 = make_password(
                        enConvenio.contraseña1)
                    enConvenio.contraseña2 = make_password(
                        enConvenio.contraseña2)
                    enConvenio.save()
                    messages.success(
                        request, "Contraseña Cambiada Correctamente")
                    return redirect('cambiar-contraseña-enc-convenio')
                else:
                    email = request.session['cuentaEncConvenio']
                    data = {
                        'email': email,
                        'error': error_message,

                    }
                return render(request, 'encargadoConvenio/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                email = request.session['cuentaEncConvenio']
                data = {
                    'email': email,
                    'error': error_message,

                }
            return render(request, 'encargadoConvenio/cambiar_contraseña.html', data)
    return render(request, "encargadoConvenio/cambiar_contraseña.html", data)


def agregar_empresa(request):
    request.session.set_expiry(10000)
    email = request.session['cuentaEncConvenio']
    empresa = Empresa.objects.all()
    data = {
        'email': email,
        'empresa': empresa,
        'form': GestionEmpresaForm()

    }
    if request.method == 'POST':
        formula = GestionEmpresaForm(data=request.POST, files=request.FILES)
        if formula.is_valid():
            formula.save()
            messages.success(request, "Empresa Agregada Correctamente")
        else:
            data["form"] = formula
    return render(request, 'encargadoConvenio/empresas/gestionarEmpresa.html', data)


def modificar_convenio(request, rut_emp):
    empresa = get_object_or_404(Empresa, rut_emp=rut_emp)
    data = {
        "form": GestionEmpresaForm(instance=empresa)
    }
    if request.method == 'POST':
        formulario = GestionEmpresaForm(data=request.POST, instance=empresa)

        if formulario.is_valid():
            formulario.save()
            return redirect(to="gestionar-empresa")
        else:
            data['form'] = formulario
    return render(request, 'encargadoConvenio/empresas/modificarEmpConv.html', data)


def eliminar_empresa(request, rut_emp):
    empresa = get_object_or_404(Empresa, rut_emp=rut_emp)
    empresa.delete()
    return redirect(to="gestionar-empresa")
# fin encargadoConvenioEmpresa

def generar_cuenta_empleado(request):
    id = request.GET["rut_emp"]
    empresa = get_object_or_404(Empresa, rut_emp=id)
    email = request.session['cuentaEncConvenio']
    data = {'empresa': empresa, 'email': email}
    if request.method == 'POST':
        nombre_cli = request.POST["nombre_cli"]
        apaterno_cli = request.POST["apaterno_cli"]
        amaterno_cli = request.POST["amaterno_cli"]
        fono_cli = request.POST["fono_cli"]
        email_cli = request.POST["email_cli"]
        #saldo_cli = postData.get('')
        empresa_rut_empresa = request.POST['empresa_rut_empresa']
        contraseña1 = request.POST["contraseña1"]
        contraseña2 = request.POST["contraseña2"]
        # validaciones
        value = {
            'nombre_cli': nombre_cli,
            'apaterno_cli': apaterno_cli,
            'amaterno_cli':amaterno_cli,
            'fono_cli':fono_cli,
            'email_cli':email_cli,
            'empresa_rut_empresa':empresa_rut_empresa,
        }
        error_message = None
        trabEmp = Cliente(nombre_cli=nombre_cli,
                          apaterno_cli=apaterno_cli,
                          amaterno_cli=amaterno_cli,
                          fono_cli=fono_cli,
                          email_cli=email_cli,
                          empresa_rut_empresa_id=empresa_rut_empresa,
                          contraseña1=contraseña1,
                          contraseña2=contraseña2)

        if len(nombre_cli) < 4:
            error_message = 'El nombre debe tener mas de 4 caracteres'
        # guadar datos de cuenta
        if not error_message:
            trabEmp.contraseña1 = make_password(trabEmp.contraseña1)
            trabEmp.contraseña2 = make_password(trabEmp.contraseña2)
            trabEmp.save()
            messages.success(request, "Cuenta Trabajador Empresa Generada")
            return redirect('gestionar-empresa')
        else:
            email = request.session['cuentaEncConvenio']
            cuentaClienteConvenio = Cliente.objects.all()
            data = {
                'email': email,
                'cuentaClienteConvenio': cuentaClienteConvenio,
                'error': error_message,
                'values': value,
            }
        return render(request, 'encargadoConvenio/cuentasEmpleados/gestionarCuentaEmpleado.html', data)
    return render(request, 'encargadoConvenio/cuentasEmpleados/gestionarCuentaEmpleado.html', data)


def listar_cuenta_empleados(request):
    id = request.GET["rut_emp"]
    cuentas_empleados = Cliente.objects.filter(empresa_rut_empresa_id=id)
    data = {'cuentas_empleados':cuentas_empleados}
    return render(request,'encargadoConvenio/cuentasEmpleados/listar_cuentas_empleados.html',data)

def editar_cuenta_trab_emp(request):
    email = request.session['cuentaEncConvenio']
    rut_cli = request.GET["rut_cli"]
    cuentaClienteConvenio = get_object_or_404(Cliente, rut_cli=rut_cli)
    data1 = {
        'email': email,
        'cuentaClienteConvenio': cuentaClienteConvenio
    }

    if request.method == "POST":
        rut_cli = request.POST["rut_cli"]
        nombre_cli = request.POST["nombre_cli"]
        apaterno_cli = request.POST["apaterno_cli"]
        amaterno_cli = request.POST["amaterno_cli"]
        fono_cli = request.POST["fono_cli"]
        email_cli = request.POST["email_cli"]
        convenio = request.POST["convenio"]
        contraseña1 = request.POST["contraseña1"]
        contraseña2 = request.POST["contraseña2"]

        cuentaClienteConvenio.rut_cli = rut_cli
        cuentaClienteConvenio.nombre_cli = nombre_cli
        cuentaClienteConvenio.apaterno_cli = apaterno_cli
        cuentaClienteConvenio.amaterno_cli = amaterno_cli
        cuentaClienteConvenio.fono_cli = fono_cli
        cuentaClienteConvenio.email_cli = email_cli
        cuentaClienteConvenio.convenio = convenio
        cuentaClienteConvenio.contraseña1 = contraseña1
        cuentaClienteConvenio.contraseña2 = contraseña2

        if(not rut_cli):
            error_message = 'El Rut es requerido'
        elif len(rut_cli) < 8:
            error_message = 'El Rut debe tener mas de 8 digitos'
        elif len(rut_cli) > 12:
            error_message = 'El Rut no debe tener mas de 12 digitos'
        elif len(nombre_cli) < 4:
            error_message = 'El nombre debe tener mas de 4 caracteres'
        elif len(apaterno_cli) < 4:
            error_message = 'El Apellido Paterno debe tener mas de 4 caracteres'
        elif len(amaterno_cli) < 4:
            error_message = 'El Apellido Materno debe tener mas de 4 caracteres'
        elif not fono_cli:
            error_message = 'El Telefono es requerido'
        elif len(fono_cli) < 8:
            error_message = 'El Telefono debe tener mas de 8 digitos'
        elif not email_cli:
            error_message = 'El email es requerido'

        elif len(contraseña1 and contraseña2) < 5:
            error_message = 'Las contraseñas deben tener mas de 5 caracteres'

        elif contraseña2 != contraseña1:
            error_message = 'Las contraseñas no coinciden'

        # guardar datos de cuenta
        if not error_message:
            cuentaClienteConvenio.save()
            messages.success(request, "Cuenta Cliente Empresa Editada")
            return redirect('editar-cuentaTrabEmp')
        else:
            email = request.session['cuentaEncConvenio']
            cuentasClienteConvenio = Cliente.objects.all()
            data = {
                'email': email,
                'cuentasClienteConvenio': cuentasClienteConvenio,
                'error': error_message,
                'cuentaClienteConvenio': cuentaClienteConvenio
            }
        return render(request, 'encargadoConvenio/cuentaEmpresas/editarCuentaTrabEmpresa', data)
    return render(request, 'encargadoConvenio/cuentaEmpresas/editarCuentaTrabEmpresa', data1)


def eliminar_cuenta_trab_emp(request, id):
    cuentaClienteConvenio = Cliente.objects.get(id=id)
    cuentaClienteConvenio.delete()
    return redirect('gestionar-cuentaTrabEmp')
# fin encargado convenio


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
        data = {'data': data, 'email': email}
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
            }
    return render(request, 'cliente/editarPerfilCliente.html', data)



#cambiar contraseña cliente
def cambiar_contraseña_cliente(request):
    check = Cliente.objects.filter(
        id_cliente=request.session['cuentaCliente'])
    if len(check) > 0:
        email = request.session['cuentaCliente']
        data = Cliente.objects.get(
            id_cliente=request.session['cuentaCliente'])
        data = {'data': data, 'email': email}
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

