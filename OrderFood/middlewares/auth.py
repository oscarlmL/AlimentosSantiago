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
