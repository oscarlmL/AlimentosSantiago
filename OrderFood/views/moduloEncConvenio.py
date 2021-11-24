from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from OrderFood.models import *
from OrderFood.forms import  *
from django.contrib import messages


# Modulo Encargado Convenio
def editar_perfil_enc_convenio(request):
    check = EncConvenio.objects.filter(
        email_enc_conv=request.session['cuentaEncConvenio'])
    if len(check) > 0:
        nombre = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
        encConvenio = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
        data = {'encConvenio': encConvenio,'nombre':nombre}
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
            nombre = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
            data = {
                'encConvenio': encConvenio,
                'error': error_message,
                'nombre':nombre

            }
    return render(request, 'trabajador/encargadoConvenio/editarPerfil.html', data)


def cambiar_contraseña_enc_convenio(request):
    check = EncConvenio.objects.filter(
        email_enc_conv=request.session['cuentaEncConvenio'])
    if len(check) > 0:
        email = request.session['cuentaEncConvenio']
        nombre = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
        encConvenio = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
        data = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
        data = {'data': data, 'email': encConvenio,'nombre':nombre}
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
                    nombre = EncConvenio.objects.get(
                        email_enc_conv=request.session['cuentaEncConvenio'])
                    data = {
                        'nombre': nombre,
                        'error': error_message,

                    }
                return render(request, 'trabajador/encargadoConvenio/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                nombre = EncConvenio.objects.get(
                    email_enc_conv=request.session['cuentaEncConvenio'])
                data = {
                    'nombre': nombre,
                    'error': error_message,

                }
            return render(request, 'trabajador/encargadoConvenio/cambiar_contraseña.html', data)
    return render(request, "trabajador/encargadoConvenio/cambiar_contraseña.html", data)


def agregar_empresa(request):
    request.session.set_expiry(10000)
    nombre = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
    empresa = Empresa.objects.all()
    data = {
        'nombre': nombre,
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
    return render(request, 'trabajador/encargadoConvenio/empresas/gestionarEmpresa.html', data)


def modificar_convenio(request, rut_emp):
    nombre = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
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


def eliminar_empresa(request, rut_emp):
    empresa = get_object_or_404(Empresa, rut_emp=rut_emp)
    empresa.delete()
    return redirect(to="gestionar-empresa")

def generar_cuenta_empleado(request):
    id = request.GET["rut_emp"]
    empresa = get_object_or_404(Empresa, rut_emp=id)
    nombre = EncConvenio.objects.get(
            email_enc_conv=request.session['cuentaEncConvenio'])
    data = {'empresa': empresa, 'nombre': nombre}
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
                email_enc_conv=request.session['cuentaEncConvenio'])
    cuentas_empleados = Cliente.objects.filter(empresa_rut_empresa_id=id)
    data = {'cuentas_empleados':cuentas_empleados,'nombre':nombre}
    return render(request,'trabajador/encargadoConvenio/cuentasEmpleados/listar_cuentas_empleados.html',data)

def editar_cuenta_trab_emp(request):
    nombre = EncConvenio.objects.get(
                email_enc_conv=request.session['cuentaEncConvenio'])
    id_cliente = request.GET["id_cliente"]
    cuentaClienteConvenio = get_object_or_404(Cliente, id_cliente=id_cliente)
    data1 = {
        'nombre': nombre,
        'cuentaClienteConvenio': cuentaClienteConvenio
    }

    if request.method == "POST":
        id_cliente = request.POST["id_cliente"]
        nombre_cli = request.POST["nombre_cli"]
        apaterno_cli = request.POST["apaterno_cli"]
        amaterno_cli = request.POST["amaterno_cli"]
        fono_cli = request.POST["fono_cli"]
        email_cli = request.POST["email_cli"]
        contraseña1 = request.POST["contraseña1"]
        contraseña2 = request.POST["contraseña2"]

        cuentaClienteConvenio.id_cliente = id_cliente
        cuentaClienteConvenio.nombre_cli = nombre_cli
        cuentaClienteConvenio.apaterno_cli = apaterno_cli
        cuentaClienteConvenio.amaterno_cli = amaterno_cli
        cuentaClienteConvenio.fono_cli = fono_cli
        cuentaClienteConvenio.email_cli = email_cli
        cuentaClienteConvenio.contraseña1 = contraseña1
        cuentaClienteConvenio.contraseña2 = contraseña2

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
            nombre = EncConvenio.objects.get(
                email_enc_conv=request.session['cuentaEncConvenio'])
            cuentasClienteConvenio = Cliente.objects.all()
            data = {
                'nombre': nombre,
                'cuentasClienteConvenio': cuentasClienteConvenio,
                'error': error_message,
                'cuentaClienteConvenio': cuentaClienteConvenio
            }
        return render(request, 'trabajador/encargadoConvenio/cuentasEmpleados/editarCuentaEmpleado.html', data)
    return render(request, 'trabajador/encargadoConvenio/cuentasEmpleados/editarCuentaEmpleado.html', data1)


def eliminar_cuenta_trab_emp(request):
    id_cliente = request.GET["id_cliente"]
    cuentaClienteConvenio = Cliente.objects.get(id_cliente=id_cliente)
    cuentaClienteConvenio.delete()
    return redirect('gestionar-empresa')
# fin encargado convenio


def cargar_saldo_cliente(request):
    return render(request,'trabajador/encargadoConvenio/cargarSaldo.html')


def leertxt(request):
    
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


    saldos = {'saldos': case_list}

    return render(request, 'trabajador/encargadoConvenio/clientesaldos.html',  saldos)
