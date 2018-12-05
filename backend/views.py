from django.shortcuts import render

# Create your views here.

def manage(request):

    return render(request, 'backend_layout.html', {})