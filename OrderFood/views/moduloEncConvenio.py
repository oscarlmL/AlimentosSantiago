from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from OrderFood.models import *
from OrderFood.forms import  *
from django.contrib import messages
from django.http import HttpResponseRedirect

# Modulo Encargado Convenio
def editar_perfil_enc_convenio(request):
    check = EncConvenio.objects.filter(
        id_enc_conv=request.session['cuentaEncConvenio'])
    if len(check) > 0:
        nombre = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
        encConvenio = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
        data = {'encConvenio': encConvenio,'nombre':nombre}
    if request.method == 'POST':
        rut_enc_conv = request.POST["rut_enc_conv"]
        nom_enc_conv = request.POST["nom_enc_conv"]
        ap_enc_conv = request.POST["ap_enc_conv"]
        email_enc_conv = request.POST["email_enc_conv"]
        celular = request.POST["celular"]

        encConvenio = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
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
            nombre = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
            data = {
                'encConvenio': encConvenio,
                'error': error_message,
                'nombre':nombre

            }
    return render(request, 'trabajador/encargadoConvenio/editarPerfil.html', data)


def cambiar_contrase??a_enc_convenio(request):
    check = EncConvenio.objects.filter(
        id_enc_conv=request.session['cuentaEncConvenio'])
    if len(check) > 0:
        email = request.session['cuentaEncConvenio']
        nombre = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
        encConvenio = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
        data = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
        data = {'data': data, 'email': encConvenio,'nombre':nombre}
    if request.method == "POST":
        contrase??a_actual = request.POST['contrase??a_actual']
        contrase??a1 = request.POST['nueva_contrase??a']
        contrase??a2 = request.POST['con_nueva_contrase??a']
        cuentaEncConvenio = EncConvenio.get_enc_convenio_by_id(email)
        if cuentaEncConvenio:
            flag = check_password(
                contrase??a_actual, cuentaEncConvenio.contrase??a1)
            error_message = None
            if flag:
                enConvenio = EncConvenio.objects.get(
                    id_enc_conv=request.session['cuentaEncConvenio'])
                enConvenio.contrase??a1 = contrase??a1
                enConvenio.contrase??a2 = contrase??a2

                error_message = None
                if len(contrase??a1 and contrase??a2) < 5:
                    error_message = 'Las contrase??as deben tener mas de 5 caracteres'
                elif len(contrase??a1 and contrase??a2) > 10:
                    error_message = 'Las contrase??as no pueden tener m??s de 10 caracteres'
                elif contrase??a2 != contrase??a1:
                    error_message = 'Las contrase??as no coinciden'

                if not error_message:
                    enConvenio.contrase??a1 = make_password(
                        enConvenio.contrase??a1)
                    enConvenio.contrase??a2 = make_password(
                        enConvenio.contrase??a2)
                    enConvenio.save()
                    messages.success(
                        request, "Contrase??a Cambiada Correctamente")
                    return redirect('cambiar-contrase??a-enc-convenio')
                else:
                    nombre = EncConvenio.objects.get(
                        id_enc_conv=request.session['cuentaEncConvenio'])
                    data = {
                        'nombre': nombre,
                        'error': error_message,

                    }
                return render(request, 'trabajador/encargadoConvenio/cambiar_contrase??a.html', data)
            else:
                error_message = 'La contrase??a actual es incorrecta'
                nombre = EncConvenio.objects.get(
                    id_enc_conv=request.session['cuentaEncConvenio'])
                data = {
                    'nombre': nombre,
                    'error': error_message,

                }
            return render(request, 'trabajador/encargadoConvenio/cambiar_contrase??a.html', data)
    return render(request, "trabajador/encargadoConvenio/cambiar_contrase??a.html", data)


# def agregar_empresa(request):
#     request.session.set_expiry(10000)
#     prueba = request.session.get(
#             'cuentaEncConvenio')
#     nombre = EncConvenio.objects.get(
#             email_enc_conv=request.session['cuentaEncConvenio'])
#     empresa = Empresa.objects.all()
#     data = {
#         'prueba':prueba,
#         'nombre': nombre,
#         'empresa': empresa,
#         'form': GestionEmpresaForm()

#     }
#     if request.method == 'POST':
#         formula = GestionEmpresaForm(request.POST)
#         if formula.is_valid():
#             formula = GestionEmpresaForm.save(commit=False)
#             formula.enc_convenio_id_enc_conv = prueba
#             formula.save()
#             messages.success(request, "Empresa Agregada Correctamente")
#         else:
#             data["form"] = formula
#     return render(request, 'trabajador/encargadoConvenio/empresas/gestionarEmpresa.html', data)


def agregar_empresa(request):
    id_enc_convenio = request.session.get(
            'cuentaEncConvenio')
    nombre = EncConvenio.objects.get(
             id_enc_conv=request.session['cuentaEncConvenio'])
    empresa = Empresa.objects.all()
    if request.method == "POST":
        form = GestionEmpresaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.enc_convenio_id_enc_conv_id = id_enc_convenio
            post.save()
            messages.success(request, "Empresa Agregada Correctamente")
            return redirect(to="gestionar-empresa")

    else:
        form = GestionEmpresaForm()
    data = {
        'empresa':empresa,
        'form':form,
        'nombre':nombre
    }
    return render(request, 'trabajador/encargadoConvenio/empresas/gestionarEmpresa.html', data)

def modificar_convenio(request, rut_emp):
    nombre = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
    empresa = get_object_or_404(Empresa, rut_emp=rut_emp)
    data = {
        "form": GestionEmpresaForm(instance=empresa),
        'nombre':nombre
    }
    if request.method == 'POST':
        formulario = GestionEmpresaForm(data=request.POST, instance=empresa)

        if formulario.is_valid():
            formulario.save()
            return redirect(to="gestionar-empresa")
        else:
            data['form'] = formulario
    return render(request, 'trabajador/encargadoConvenio/empresas/modificarEmpConv.html', data)


def eliminar_empresa(request):
    rut_emp = request.GET["rut_emp"]
    empresa = get_object_or_404(Empresa, rut_emp=rut_emp)
    empresa.delete()
    messages.success(request, "Empresa Eliminada Correctamente")
    return redirect(to="gestionar-empresa")

def generar_cuenta_empleado(request):
    id = request.GET["rut_emp"]
    empresa = get_object_or_404(Empresa, rut_emp=id)
    nombre = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
    data = {'empresa': empresa, 'nombre': nombre}
    if request.method == 'POST':
        email_cli = request.POST["email_cli"]
        empresa_rut_empresa = request.POST['empresa_rut_empresa']
        contrase??a1 = request.POST["contrase??a1"]
        contrase??a2 = request.POST["contrase??a2"]
        # validaciones
        value = {
            'email_cli':email_cli,
            'empresa_rut_empresa':empresa_rut_empresa,
        }
        error_message = None
        trabEmp = Cliente(
                          email_cli=email_cli,
                          empresa_rut_empresa_id=empresa_rut_empresa,
                          contrase??a1=contrase??a1,
                          contrase??a2=contrase??a2)

        # guadar datos de cuenta
        if not error_message:
            trabEmp.contrase??a1 = make_password(trabEmp.contrase??a1)
            trabEmp.contrase??a2 = make_password(trabEmp.contrase??a2)
            trabEmp.save()
            messages.success(request, "Cuenta Trabajador Empresa Generada")
            return redirect('gestionar-empresa')
        else:
            nombre = EncConvenio.objects.get(
                email_enc_conv=request.session['cuentaEncConvenio'])
            cuentaClienteConvenio = Cliente.objects.all()
            data = {
                'nombre': nombre,
                'cuentaClienteConvenio': cuentaClienteConvenio,
                'error': error_message,
                'values': value,
                'empresa':empresa
            }
        return render(request, 'trabajador/encargadoConvenio/cuentasEmpleados/gestionarCuentaEmpleado.html', data)
    return render(request, 'trabajador/encargadoConvenio/cuentasEmpleados/gestionarCuentaEmpleado.html', data)


def listar_cuenta_empleados(request):
    id = request.GET["rut_emp"]
    nombre = EncConvenio.objects.get(
                id_enc_conv=request.session['cuentaEncConvenio'])
    cuentas_empleados = Cliente.objects.filter(empresa_rut_empresa_id=id)
    data = {'cuentas_empleados':cuentas_empleados,'nombre':nombre}
    return render(request,'trabajador/encargadoConvenio/cuentasEmpleados/listar_cuentas_empleados.html',data)

def editar_cuenta_trab_emp(request):
    nombre = EncConvenio.objects.get(
                id_enc_conv=request.session['cuentaEncConvenio'])
    id_cliente = request.GET["id_cliente"]
    cuentaClienteConvenio = get_object_or_404(Cliente, id_cliente=id_cliente)
    data1 = {
        'nombre': nombre,
        'cuentasClienteConvenio': cuentaClienteConvenio
    }

    if request.method == "POST":
        nombre_cli = request.POST["nombre_cli"]
        apaterno_cli = request.POST["apaterno_cli"]
        amaterno_cli = request.POST["amaterno_cli"]
        fono_cli = request.POST["fono_cli"]
        email_cli = request.POST["email_cli"]

        cuentaClienteConvenio.nombre_cli = nombre_cli
        cuentaClienteConvenio.apaterno_cli = apaterno_cli
        cuentaClienteConvenio.amaterno_cli = amaterno_cli
        cuentaClienteConvenio.fono_cli = fono_cli
        cuentaClienteConvenio.email_cli = email_cli

        error_message = None
        if len(nombre_cli) < 4:
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

        # guardar datos de cuenta
        if not error_message:
            cuentaClienteConvenio.save()
            messages.success(request, "Cuenta Trabajador Empresa Editada")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            nombre = EncConvenio.objects.get(
                id_enc_conv=request.session['cuentaEncConvenio'])
            cuentasClienteConvenio = Cliente.objects.all()
            data = {
                'nombre': nombre,
                'cuentasClienteConvenio': cuentasClienteConvenio,
                'error': error_message,
                'cuentasClienteConvenio': cuentaClienteConvenio
            }
        return render(request, 'trabajador/encargadoConvenio/cuentasEmpleados/editarCuentaEmpleado.html', data)
    return render(request, 'trabajador/encargadoConvenio/cuentasEmpleados/editarCuentaEmpleado.html', data1)


def eliminar_cuenta_trab_emp(request):
    id_cliente = request.GET["id_cliente"]
    cuentaClienteConvenio = Cliente.objects.get(id_cliente=id_cliente)
    cuentaClienteConvenio.delete()
    messages.success(request, "Trabajador Eliminado Correctamente")
    return redirect('gestionar-empresa')
# fin encargado convenio


def cargar_saldo_cliente(request):
    nombre = EncConvenio.objects.get(
             id_enc_conv=request.session['cuentaEncConvenio'])
    data = {'nombre':nombre}
    return render(request,'trabajador/encargadoConvenio/cargarSaldo.html',data)


def leertxt(request):
    nombre = EncConvenio.objects.get(
             id_enc_conv=request.session['cuentaEncConvenio'])
    data = request.FILES['file'].readlines()
    case_list = []
    for a in data:

        fila = str(a).split(';')
        rut = str(fila[0]).replace("'", "")
        rut = rut.replace("b", "")
        saldo = str(fila[1]).replace("'", "")
        saldo = saldo.replace(r'\n', ' ').replace(r'\r', '')

        existe = Cliente.objects.filter(empresa_rut_empresa_id=rut).count()

        if existe > 0 :
            cliente = Cliente.objects.get(empresa_rut_empresa_id=rut)
            #print(cliente)
            #print('el valor es : '+ rut + 'su saldo es: ' + saldo)

            saldonuevo = int(cliente.saldo_cli) + int(saldo)

            Cliente.objects.filter(empresa_rut_empresa_id=rut).update(saldo_cli=saldonuevo)

            case = {'rut_empresa':cliente.empresa_rut_empresa,'nombre': cliente.nombre_cli, 'paterno': cliente.apaterno_cli, 'materno': cliente.amaterno_cli, 'saldoactual': cliente.saldo_cli, 'saldo': saldo, 'saldonuevo': saldonuevo }
            case_list.append(case)


    saldos = {'saldos': case_list,
    'nombre':nombre}

    return render(request, 'trabajador/encargadoConvenio/clientesaldos.html',  saldos)
