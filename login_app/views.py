from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request , 'index.html' )

def register(request):
    if request.method == 'POST':
       errors = User.objects.basic_validator(request.POST)

       if len(errors) > 0:
           for msg in errors.values():
               messages.error(request , msg)
           return  redirect('/')
       
       else:
            user = User.objects.create_user(request.POST)
            request.session['user_id']=user.id

            return redirect('/books')
    
    return  redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if errors:
            for msg in errors.values():
                messages.error(request, msg)
            return redirect('/')
        user = User.objects.filter(email=request.POST.get('email', ''))[0]
        request.session['user_id'] = user.id
        return redirect('/books')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')