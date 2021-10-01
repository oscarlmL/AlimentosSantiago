from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django import views
from .models import *


# Create your views here.

def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def generar_cuenta_enc_cocina(request):
    if request.method == 'GET':
        return render(request, 'generarCuenta.html')
    else:
        postData = request.POST
        nom_enc_coc = postData.get('nombre')
        titulo = postData.get('titulo')
        exp_laboral = postData.get('experiencia_laboral')
        email_enc_coc = postData.get('email_enc_cocina')
        contraseña1 = postData.get('contraseña1')
        contraseña2 = postData.get('contraseña2')

        # validaciones
        value = {
            'nom_enc_coc': nom_enc_coc,
            'titulo': titulo,
            'exp_laboral': exp_laboral,
            'email_enc_coc': email_enc_coc,
        }
        error_message = None
        encCocina = EncCocina(nom_enc_coc=nom_enc_coc,
                              titulo=titulo,
                              exp_laboral=exp_laboral,
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
            return redirect('generar-cuenta')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'generarCuenta.html', data)
