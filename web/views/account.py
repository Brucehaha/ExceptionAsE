from django.shortcuts import render, HttpResponse, redirect
from utils.recaptcha import recaptcha
from io import BytesIO
from ..forms.account import LoginForm
from repository import models
import json


def check_code(request):
    bcache = BytesIO()
    image, code = recaptcha()
    image.save(bcache, 'png')
    request.session['recapcha_code']=code
    return HttpResponse(bcache.getvalue())

def logout(request):
    request.session.clear()
    return redirect('/')


def login(request):
    """
    login
    :param request:
    :return: http
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        data = {"status": False, 'message': None,}
        form_obj = LoginForm(request=request, data=request.POST)
        if form_obj.is_valid():
            email = form_obj.cleaned_data.get('email')
            password = form_obj.cleaned_data.get('password')
            user_info = models.UserInfo.objects.\
                        filter(email=email, password=password).\
                        values("nid","username", "email", "avatar", "blog__nid", 'blog__site').first()
            if user_info:
                data['status']=True
                data['message'] = "thank you"
                request.session['user_info']=user_info
                if form_obj.cleaned_data.get('month'):
                    print(form_obj.cleaned_data.get('month'))
                    request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                data['message'] = 'email or password is incorrect'
        else:
            if 'check_code' in form_obj.errors:
                data['message'] = 'Authentication code is wrong'
            else:
                data['message'] = 'email or password is incorrect'

        return HttpResponse(json.dumps(data))




