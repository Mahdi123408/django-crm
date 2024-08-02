from django.http import HttpRequest
from custom_auth.models import User


def check_auth(request: HttpRequest):
    if 'username' and 'password' in request.session:
        username = request.session['username']
        password = request.session['password']
        user = User.objects.filter(username=username, active=True).first()
        if user and user.check_password(password):
            return [True, user]
        else:
            del request.session['username']
            del request.session['password']
            request.session['mes'] = 'خروج با موفقیت انجام شد وارد شوید'
            return [False, 'username or password incorrect']
    else:
        return [False, 'not logged in']


def login(request: HttpRequest, username: str, password: str):
    user = User.objects.filter(username=username, active=True).first()
    if user and user.check_password(password):
        request.session['username'] = username
        request.session['password'] = password
        return True, user
    else:
        return False, 'username or password incorrect'
