from django.shortcuts import redirect


def auth_middleware(get_response):
    def middleware(request):
        print(request.session.get('cuentaAdmin'))
        if not request.session.get('cuentaAdmin'):            
            return redirect('login')
        response = get_response(request)
        return response
    return middleware

def auth_middleware_enc_cocina(get_response):
    def middleware(request):
        print(request.session.get('cuentaEncCocina'))
        if not request.session.get('cuentaEncCocina'):            
            return redirect('login')
        response = get_response(request)
        return response
    return middleware

def auth_middleware_enc_convenio(get_response):
    def middleware(request):
        print(request.session.get('cuentaEncConvenio'))
        if not request.session.get('cuentaEncConvenio'):            
            return redirect('login')
        response = get_response(request)
        return response
    return middleware

def auth_middleware_repartidor(get_response):
    def middleware(request):
        print(request.session.get('cuentaRepartidor'))
        if not request.session.get('cuentaRepartidor'):            
            return redirect('login')
        response = get_response(request)
        return response
    return middleware

def auth_middleware_cliente(get_response):
    def middleware(request):
        print(request.session.get('cuentaCliente'))
        if not request.session.get('cuentaCliente'):            
            return redirect('login')
        response = get_response(request)
        return response
    return middleware

def auth_middleware_cajero(get_response):
    def middleware(request):
        print(request.session.get('cuentaCajero'))
        if not request.session.get('cuentaCajero'):            
            return redirect('login')
        response = get_response(request)
        return response
    return middleware

