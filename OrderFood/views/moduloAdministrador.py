from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django import views
from OrderFood.models import *
from django.views import View
from django.contrib import messages
from OrderFood.forms import  *



# Modulo administracion
def editar_perfil_admin(request):
    check = Administrador.objects.filter(
        email_admin=request.session['cuentaAdmin'])
    if len(check) > 0:
        nombre = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin'])
        admin = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin'])
        data = {'admin': admin, 'nombre': nombre}
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
            nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])
            data = {
                'nombre': nombre,
                'error': error_message,
                'admin':admin
            }
    return render(request, 'trabajador/administrador/editarPerfil.html', data)


def cambiar_contraseña_admin(request):
    check = Administrador.objects.filter(
        email_admin=request.session['cuentaAdmin'])
    if len(check) > 0:
        nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])
        email = request.session['cuentaAdmin']
        data = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin'])
        data = {'data': data, 'email': email,'nombre':nombre}
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
                    nombre = Administrador.objects.get(
                            email_admin=request.session['cuentaAdmin'])
                    data = {
                        'nombre': nombre,
                        'error': error_message,

                    }
                return render(request, 'trabajador/administrador/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                nombre = Administrador.objects.get(
                    email_admin=request.session['cuentaAdmin'])
                data = {
                    'nombre': nombre,
                    'error': error_message,

                }
            return render(request, 'trabajador/administrador/cambiar_contraseña.html', data)
    return render(request, "trabajador/administrador/cambiar_contraseña.html", data)


def generar_cuenta_enc_cocina(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        nombre = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin'])        
        cuentasEncCocina = EncCocina.objects.all()
        data = {
            'nombre': nombre,
            'cuentasEncCocina': cuentasEncCocina
        }
        return render(request, 'trabajador/administrador/cuenta/encargadoCocina/gestionarEncCocina.html', data)
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
            nombre = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin']) 
            cuentasEncCocina = EncCocina.objects.all()
            data = {
                'nombre': nombre,
                'cuentasEncCocina': cuentasEncCocina,
                'error': error_message,
                'values': value,
            }
        return render(request, 'trabajador/administrador/cuenta/encargadoCocina/gestionarEncCocina.html', data)


def editar_cuenta_enc_cocina(request):
    nombre = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin']) 
    id_enc_coc = request.GET["id_enc_coc"]
    cuentaEncCocina = get_object_or_404(EncCocina, id_enc_coc=id_enc_coc)
    data1 = {
        'nombre': nombre,
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
            nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])             
            cuentasEncCocina = EncCocina.objects.all()
            data = {
                'nombre': nombre,
                'cuentasEncCocina': cuentasEncCocina,
                'error': error_message,
                'cuentaEncCocina': cuentaEncCocina
            }
        return render(request, 'trabajador/administrador/cuenta/encargadoCocina/edicionEncCocina.html', data)
    return render(request, 'trabajador/administrador/cuenta/encargadoCocina/edicionEncCocina.html', data1)


def eliminar_cuenta_enc_cocina(request):
    id_enc_coc = request.GET["id_enc_coc"]
    cuentasEncCocina = EncCocina.objects.get(id_enc_coc=id_enc_coc)
    cuentasEncCocina.delete()
    return redirect('gestionar-encCocina')


def generar_cuenta_enc_convenio(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])         
        cuentasEncConvenio = EncConvenio.objects.all()
        data = {
            'cuentasEncConvenio': cuentasEncConvenio,
            'nombre': nombre
        }
        return render(request, 'trabajador/administrador/cuenta/encargadoConvenio/gestionarEncConvenio.html', data)
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
            nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])
            cuentasEncConvenio = EncConvenio.objects.all()
            data = {
                'nombre': nombre,
                'cuentasEncConvenio': cuentasEncConvenio,
                'error': error_message,
                'values': value,
            }
        return render(request, 'trabajador/administrador/cuenta/encargadoConvenio/gestionarEncConvenio.html', data)


def editar_cuenta_enc_convenio(request):
    nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])    
    id_enc_conv = request.GET["id_enc_conv"]
    cuentaEncConvenio = get_object_or_404(EncConvenio, id_enc_conv=id_enc_conv)
    data1 = {
        'nombre': nombre,
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
            nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])             
            cuentasEncConvenio = EncConvenio.objects.all()
            data = {
                'nombre': nombre,
                'error': error_message,
                'cuentasEncConvenio': cuentasEncConvenio,
                'cuentaEncConvenio': cuentaEncConvenio
            }
        return render(request, 'trabajador/administrador/cuenta/encargadoConvenio/edicionEncConvenio.html', data)
    return render(request, 'trabajador/administrador/cuenta/encargadoConvenio/edicionEncConvenio.html', data1)



def eliminar_cuenta_enc_convenio(request):
    id_enc_conv = request.GET["id_enc_conv"]
    cuentaEncConvenio = EncConvenio.objects.get(id_enc_conv=id_enc_conv)
    cuentaEncConvenio.delete()
    return redirect('gestionar-enc-convenio')


def generar_cuenta_repartidor(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin']) 
        cuentasRepartidor = Repartidor.objects.all()
        data = {
            'cuentasRepartidor': cuentasRepartidor,
            'nombre': nombre
        }
        return render(request, 'trabajador/administrador/cuenta/repartidor/gestionarRepartidor.html', data)
    else:
        postData = request.POST
        rut_repartidor = postData.get('rut_repartidor')
        nombre_repartidor = postData.get('nombre_repartidor')
        apellido_repartidor = postData.get('apellido_repartidor')
        email_repartidor = postData.get('email_repartidor')
        tipo_veh = postData.get('tipo_veh')
        patente_veh_moto = postData.get('patente_veh_moto')
        patente_veh_auto = postData.get('patente_veh_auto')
        bicicleta = postData.get('bicicleta')
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
                                    patente_veh_auto or patente_veh_moto or bicicleta),
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
            nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])
            cuentasRepartidor = Repartidor.objects.all()
            data = {
                'nombre': nombre,
                'cuentasRepartidor': cuentasRepartidor,
                'error': error_message,
                'values': value
            }
        return render(request, 'trabajador/administrador/cuenta/repartidor/gestionarRepartidor.html', data)


def editar_cuenta_repartidor(request):
    nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])
    id_repartidor = request.GET["id_repartidor"]
    cuentaRepartidor = get_object_or_404(
        Repartidor, id_repartidor=id_repartidor)
    data1 = {
        'nombre': nombre,
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
        bicicleta = request.POST['bicicleta']
        celular = request.POST['celular']

        cuentaRepartidor.rut_repartidor = rut_repartidor
        cuentaRepartidor.nombre_repartidor = nombre_repartidor
        cuentaRepartidor.apellido_repartidor = apellido_repartidor
        cuentaRepartidor.email_repartidor = email_repartidor
        cuentaRepartidor.tipo_veh = tipo_veh
        cuentaRepartidor.patente_veh = (patente_veh_moto or patente_veh_auto or bicicleta)
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
            nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])
            cuentasRepartidor = Repartidor.objects.all()
            data = {
                'nombre': nombre,
                'error': error_message,
                'cuentasRepartidor': cuentasRepartidor,
                'cuentaRepartidor': cuentaRepartidor
            }
        return render(request, 'trabajador/administrador/cuenta/repartidor/edicionRepartidor.html', data)
    return render(request, 'trabajador/administrador/cuenta/repartidor/edicionRepartidor.html', data1)


def eliminar_cuenta_repartidor(request):
    id_repartidor = request.GET["id_repartidor"]
    cuentaRepartidor = get_object_or_404(
        Repartidor, id_repartidor=id_repartidor)
    cuentaRepartidor.delete()
    return redirect('gestionar-repartidor')

def generar_cuenta_cajero(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])        
        cuentaCajero = Cajero.objects.all()
        cajero_rest = Restaurant.objects.all()
        data = {
            'cuentasCajero': cuentaCajero,
            'nombre': nombre,
            'cajero_rest':cajero_rest
        }
        return render(request, 'trabajador/administrador/cuenta/cajero/gestionarCajero.html', data)
    else:
        postData = request.POST
        nom_cajero = postData.get('nom_cajero')
        email_cajero = postData.get('email_cajero')
        restaurante = postData.get('restaurante')
        contraseña1 = postData.get('contraseña1')
        contraseña2 = postData.get('contraseña2')

        # validaciones
        value = {
            'nom_cajero': nom_cajero,
            'email_cajero': email_cajero,
            'contraseña1': contraseña1,
            'contraseña2':contraseña2
            }
        error_message = None
        cajero = Cajero(nom_cajero=nom_cajero,
                            email_cajero=email_cajero,
                            restaurante_id = restaurante,
                            contraseña1=contraseña1,
                            contraseña2=contraseña2
        )
        if not nom_cajero:
            error_message = 'El Nombre es requerido'
        elif len(nom_cajero) < 4:
            error_message = 'El Nombre debe tener mas de 4 caracteres'

        elif len(contraseña1 and contraseña2) < 5:
            error_message = 'Las contraseñas deben tener mas de 5 caracteres'

        elif len(contraseña1 and contraseña2) > 10:
            error_message = 'Las contraseñas no puede ser mayor a 10 caracteres'

        elif contraseña2 != contraseña1:
            error_message = 'Las contraseñas no coinciden'

        elif not email_cajero:
            error_message = 'El email es requerido'

        elif cajero.emailExiste():
            error_message = 'El email ya tiene una cuenta'

        # guardar datos de cuenta
        if not error_message:
            cajero.contraseña1 = make_password(cajero.contraseña1)
            cajero.contraseña2 = make_password(cajero.contraseña2)
            cajero.cuentaCajero()
            messages.success(request, "Cuenta Cajero Generada")
            return redirect('gestionar-cajero')
        else:
            nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])              
            cuentasCajero = Cajero.objects.all()
            data = {
                'nombre': nombre,
                'cuentasCajero': cuentasCajero,
                'error': error_message,
                'values': value
            }
        return render(request, 'trabajador/administrador/cuenta/cajero/gestionarCajero.html', data)

def editar_cuenta_cajero(request):
    nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])     
    id_cajero = request.GET["id_cajero"]
    cuentaCajero = get_object_or_404(
        Cajero, id_cajero=id_cajero)
    data1 = {
        'nombre': nombre,
        'cuentaCajero': cuentaCajero
    }
    if request.method == "POST":
        nom_cajero = request.POST['nom_cajero']
        email_cajero = request.POST['email_cajero']

        cuentaCajero.nom_cajero = nom_cajero
        cuentaCajero.email_cajero = email_cajero

        error_message = None
        if not cuentaCajero.nom_cajero:
            error_message = 'El Nombre es requerido'
        elif len(cuentaCajero.nom_cajero) < 4:
            error_message = 'El Nombre debe tener mas de 4 caracteres'
        elif not cuentaCajero.email_cajero:
            error_message = 'El email es requerido'

        # guardar datos de cuenta
        if not error_message:
            cuentaCajero.save()
            messages.success(request, "Cuenta Cajero Editada")
            return redirect('gestionar-cajero')
        else:
            nombre = Administrador.objects.get(
                email_admin=request.session['cuentaAdmin'])             
            cuentasCajero = Cajero.objects.all()
            data = {
                'nombre': nombre,
                'error': error_message,
                'cuentasCajero': cuentasCajero,
                'cuentaCajero': cuentaCajero
            }
        return render(request, 'trabajador/administrador/cuenta/cajero/edicionCajero.html', data)
    return render(request, 'trabajador/administrador/cuenta/cajero/edicionCajero.html', data1)

def eliminar_cuenta_cajero(request):
    id_cajero = request.GET["id_cajero"]
    cuentaCajero = get_object_or_404(
        Cajero, id_cajero=id_cajero)
    cuentaCajero.delete()
    return redirect('gestionar-cajero')


# pedidos trabajador // cambiar de cliente a trabajador
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

    return render(request, 'trabajador/pedido/agregar.html', data)


def listar_pedido(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    data = {
        'pedidos': pedidos
    }

    return render(request, 'trabajador/pedido/listar.html', data)


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

    return render(request, 'trabajador/pedido/modificar.html', data)


def eliminar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id_pedido=id)
    pedido.delete()
    return redirect(to="listar_pedido")
# fin pedido
