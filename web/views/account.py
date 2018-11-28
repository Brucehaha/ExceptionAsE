from django.shortcuts import render, HttpResponse
from utils.recaptcha import recaptcha
from io import BytesIO

def login(request):
    return render(request, 'login.html',{})


def check_code(request):
    bcache = BytesIO()
    image, code = recaptcha()
    image.save(bcache, 'png')
    request.session['recapcha_code']=code

    return HttpResponse(bcache.getvalue())
