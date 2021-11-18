from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from OrderFood.models import *
from OrderFood.forms import  *
from django.contrib import messages

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
    return render(request, 'trabajador/encargadoCocina/editarPerfil.html', data)


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
                return render(request, 'trabajador/encargadoCocina/cambiar_contraseña.html', data)
            else:
                error_message = 'La contraseña actual es incorrecta'
                email = request.session['cuentaEncCocina']
                data = {
                    'email': email,
                    'error': error_message,

                }
            return render(request, 'trabajador/encargadoCocina/cambiar_contraseña.html', data)
    return render(request, "trabajador/encargadoCocina/cambiar_contraseña.html", data)


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

    return render(request, 'trabajador/encargadoCocina/menu/gestionarPlato.html', data)


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

    return render(request, 'trabajador/encargadoCocina/menu/modificar.html', data)


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

    return render(request, 'trabajador/encargadoCocina/proveedor/contactoProveedor.html', data)


def listar_proveedor(request):
    request.session.set_expiry(10000)
    email = request.session['cuentaEncCocina']
    proveedores = Proveedor.objects.all()
    data = {
        'proveedores': proveedores,
        'email': email
    }
    return render(request, 'trabajador/encargadoCocina/proveedor/listar.html', data)


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

    return render(request, 'trabajador/encargadoCocina/proveedor/modificar.html', data)


def eliminar_proveedor(request):
    id_proveedor = request.GET["id_proveedor"]
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    proveedor.delete()
    messages.success(request, "Eliminación exitosa")
    return redirect(to="listar_proveedor")


# Modulo Restaurant
def restaurant(request):
    restaurantes = Restaurant.objects.all()
    data = {
        'form': RestaurantForm(),
        'restaurantes': restaurantes
    }
    if request.method == 'POST':
        formulario = RestaurantForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Restaurant guardado correctamente")
        else:
            data["form"] = formulario

    return render(request, 'trabajador/encargadoCocina/restaurant/gestionarRestaurant.html', data)


def listar_restaurant(request):
    request.session.set_expiry(10000)
    email = request.session['cuentaEncCocina']
    restaurantes = Restaurant.objects.all()
    data = {
        'restaurantes': restaurantes,
        'email': email
    }
    return render(request, 'trabajador/encargadoCocina/restaurant/gestionarRestaurant.html', data)


def modificar_restaurant(request):
    request.session.set_expiry(10000)
    email = request.session['cuentaEncCocina']
    id_restaurante = request.GET["id_restaurante"]
    restaurant = get_object_or_404(Restaurant, id_restaurante=id_restaurante)

    data = {
        'email': email,
        'form': RestaurantForm(instance=restaurant),
        
        # 'restaurant': restaurant
    }

    if request.method == 'POST':
        formulario = RestaurantForm(data=request.POST, instance=restaurant, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificación exitosa")
            return redirect(to="restaurant")
        data["form"] = formulario

    return render(request, 'trabajador/encargadoCocina/restaurant/modificarRestaurant.html', data)


def eliminar_restaurant(request):
    id_restaurante = request.GET["id_restaurante"]
    restaurant = get_object_or_404(Restaurant, id_restaurante=id_restaurante)
    restaurant.delete()
    messages.success(request, "Eliminación exitosa")
    return redirect(to="restaurant")


# Fin modulo encargado Cocina