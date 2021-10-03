from django.contrib.messages.storage.base import Message
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django import views
from .models import *
from django.views import View
from django.contrib import messages

# Create your views here.

def home(request):
    email = request.session.get('cuentaAdmin') or request.session.get(
    'cuentaEncConvenio') or request.session.get('cuentaEncCocina')
    return render(request, 'home.html', {'email': email})

def generar_cuenta_get(request):
    email = request.session.get('cuentaAdmin')
    return render(request, 'generarCuenta.html', {'email': email})


def generar_cuenta_enc_cocina(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        email = request.session['cuentaAdmin']
        return render(request, 'encargadoCocina.html', {'email': email})
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

        # gudar datos de cuenta
        if not error_message:
            encCocina.contraseña1 = make_password(encCocina.contraseña1)
            encCocina.contraseña2 = make_password(encCocina.contraseña2)
            encCocina.cuentaEncargadoCocina()
            messages.success(request, "Cuenta Encargado Cocina Generada")
            return redirect('encargado-cocina')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'encargadoCocina.html', data)


def generar_cuenta_enc_convenio(request):
    request.session.set_expiry(10000)
    if request.method == 'GET':
        email = request.session['cuentaAdmin']
        return render(request, 'encargadoConvenio.html', {'email': email})
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
            return redirect('encargado-convenio')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'encargadoConvenio.html', data)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        cuentaAdmin = Administrador.get_admin_by_email(email)
        cuentaEncCocina = EncCocina.get_enc_cocina_by_email(email)
        cuentaEncConvenio = EncConvenio.get_enc_convenio_by_email(email)
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
            flag = check_password(contraseña, cuentaEncCocina.contraseña1),
            if flag:
                request.session['cuentaEncCocina'] = cuentaEncCocina.email_enc_coc
                print('eres: ', email)
                return redirect('home')
        elif cuentaEncConvenio:
            flag = check_password(contraseña, cuentaEncConvenio.contraseña1),
            if flag:
                request.session['cuentaEncConvenio'] = cuentaEncConvenio.email_enc_conv
                print('eres: ', email)
                return redirect('home')
        else:
            error_message = 'Email o Contraseña incorrecto'
        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')
