from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from my_methods.auth import check_auth, login


class LoginView(View):
    def get(self, request: HttpRequest):
        user = check_auth(request)
        if user[0]:
            return redirect('user')
        else:
            mes = None
            if 'mes' in request.session:
                mes = request.session.get('mes')
                del request.session['mes']
            return render(request, 'auth/login/login.html', {'mes': mes})

    def post(self, request):
        user = check_auth(request)
        if user[0]:
            return redirect('user')
        else:
            if 'username' in request.POST and 'password' in request.POST:
                check_login = login(request, request.POST['username'], request.POST['password'])
                if check_login[0]:
                    return redirect('user')
                else:
                    request.session['mes'] = 'نام کاربری یا رمز  عبور اشتباه است .'
                    return redirect('login')


def logout(request: HttpRequest):
    user = check_auth(request)
    if user[0]:
        del request.session['username']
        del request.session['password']
        request.session['mes'] = 'خروج با موفقیت انجام شد وارد شوید'
        return redirect('login')
    else:
        return redirect('login')
