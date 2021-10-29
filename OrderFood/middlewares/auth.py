from django.shortcuts import redirect


def auth_middleware(get_response):
    def middleware(request):
        print(request.session.get('cuentaAdmin'))
        if not request.session.get('cuentaAdmin'):            
            return redirect('login')
        response = get_response(request)
        return response
    return middleware

