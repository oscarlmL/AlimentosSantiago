from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404,HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from OrderFood.models import *
from django.views import View
from django.db.models import Q
from django.http import HttpResponseRedirect
from OrderFood.filters import buscarPlato


def incio_trabajador(request):
    if request.session.get('cuentaAdmin'):
        nombre = Administrador.objects.get(
            email_admin=request.session['cuentaAdmin'])
        return render(request,'trabajador/inicio_trabajador.html',{'nombre':nombre})
    elif request.session.get('cuentaEncConvenio'):
        nombre = EncConvenio.objects.get(
            id_enc_conv=request.session['cuentaEncConvenio'])
        return render(request,'trabajador/inicio_trabajador.html',{'nombre':nombre})
    elif request.session.get('cuentaEncCocina'):
        nombre = EncCocina.objects.get(
            email_enc_coc=request.session['cuentaEncCocina'])
        return render(request,'trabajador/inicio_trabajador.html',{'nombre':nombre})
    elif request.session.get('cuentaRepartidor'):
        nombre = Repartidor.objects.get(
            id_repartidor=request.session['cuentaRepartidor'])
        return render(request,'trabajador/inicio_trabajador.html',{'nombre':nombre})
    elif request.session.get('cuentaCajero'):
        nombre = Cajero.objects.get(
                email_cajero=request.session['cuentaCajero'])  
        return render(request,'trabajador/inicio_trabajador.html',{'nombre':nombre})

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
        cuentaCajero = Cajero.get_cajero_by_email(email)
        error_message = None
        if cuentaAdmin:
            flag = check_password(contraseña, cuentaAdmin.contraseña1)
            if flag:
                request.session['cuentaAdmin'] = cuentaAdmin.email_admin
                print('eres: ', email)
                return redirect('incio_trabajador')
            else:
                error_message = 'Email o Contraseña incorrecto'
        elif cuentaEncCocina:
            flag = check_password(contraseña, cuentaEncCocina.contraseña1)
            if flag:
                request.session['cuentaEncCocina'] = cuentaEncCocina.email_enc_coc
                print('eres: ', email)
                return redirect('incio_trabajador')
            else:
                error_message = 'Email o Contraseña incorrecto'
        elif cuentaEncConvenio:
            flag = check_password(contraseña, cuentaEncConvenio.contraseña1)
            if flag:
                request.session['cuentaEncConvenio'] = cuentaEncConvenio.id_enc_conv
                print('eres :', email)
                return redirect('incio_trabajador')
            else:
                error_message = 'Email o Contraseña incorrecto'
        elif cuentaRepartidor:
            flag = check_password(contraseña, cuentaRepartidor.contraseña1)
            if flag:
                request.session['cuentaRepartidor'] = cuentaRepartidor.id_repartidor
                print('eres :', email, cuentaRepartidor.id_repartidor)
                return redirect('incio_trabajador')
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
        elif cuentaCajero:
            flag = check_password(contraseña, cuentaCajero.contraseña1)
            if flag:
                request.session['cuentaCajero'] = cuentaCajero.email_cajero
                print('eres :',email)
                return redirect('incio_trabajador')
            else:
                error_message = 'Email o Contraseña incorrecto'
        error_message = 'Email o Contraseña incorrecto'
        return render(request, 'login.html', {'error': error_message})

class home(View):
    def post(self,request):
        #PLATO ES EL NOMBRE QUE SE LE DA AL BOT
        resta = request.POST.get('resta')
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
        return redirect('platos/'+ resta)

    def get(self, request):
        if request.session.get('cuentaCliente'):
            clienteeee = Cliente.objects.get(id_cliente=request.session['cuentaCliente'])
            carro = request.session.get('carro')
            if not carro:
                request.session['carro'] = {}
            restaurant = Restaurant.objects.all()
            context = {
                'restaurant':restaurant,
                'clienteeee':clienteeee
                }
            request.session['carro'] = {}
            return render(request, 'cliente/home.html', context)
        else:
            carro = request.session.get('carro')
            if not carro:
                request.session['carro'] = {}
            restaurant = Restaurant.objects.all()
            context = {
                    'restaurant':restaurant,
            }
            request.session['carro'] = {}
            return render(request, 'cliente/home.html', context)


  
def eliminar_plato_carro(request):
    plato_carro = request.POST.get('plato_carro')
    list_cart  = request.session['carro']
    list_cart.pop(plato_carro)
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def limpiar_carro(request):
    request.session['carro'] = {}
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def listar_plato_restaurante(request,id_restaurante):
    platos = Plato.objects.filter(Restaurant_id=id_restaurante)
    #MODAL CARRITO
    id_plato = (list(request.session.get('carro').keys()))
    platos_en_carro = Plato.get_plato_by_id_plato(id_plato)
    print(platos_en_carro)
    #FIN MODAL CARRITO
    myfilter = buscarPlato(request.GET, queryset=platos)
    platos = myfilter.qs
    data = {
        'myfilter':myfilter,
        'platos': platos,
        'platos_en_carro':platos_en_carro,
        'categoria':reversed(categoriaPlato.objects.all()),
        'platos_categoria':reversed(categoriaPlato.objects.all()),
    }
    return render(request, 'cliente/platos.html', data)



# Funciones Generales
def buscar_plato(request):
    busqueda = request.GET.get("buscar")
    platos = Plato.objects-all()

    if busqueda:
        platos = Plato.objects.filter(
            Q(nom_plato__icontains = busqueda) |
            Q(valor_plato__icontains = busqueda) |
            Q(descripcion__icontains = busqueda) |
            Q(Restaurant__icontains = busqueda) 
        ).distinc()

    return render(request,'home.html', {'platos': platos})

def logout(request):
    request.session.clear()
    return redirect('home')
