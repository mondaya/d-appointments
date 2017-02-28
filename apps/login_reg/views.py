from django.shortcuts import render, redirect,HttpResponse
from models import User

from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'login_reg/index.html')

def registration(request):
    if request.method == "POST":
        model_rsp = User.objects.registration(request.POST)  
        if  model_rsp['status']:
            request.session['user_id'] = model_rsp['user'].id
            request.session['user'] = model_rsp['user'].first_name            
            return redirect('home:success')
        else:
            for error in model_rsp['errors']:
                messages.error(request, error)
    return redirect('home:signup')
                
def login(request):

    if request.method == 'POST': 
        model_rsp = User.objects.login(request.POST)
        if  model_rsp['status']:
            request.session['user_id'] = model_rsp['user'].id
            request.session['user'] = model_rsp['user'].first_name            
            return redirect('home:success')
        else:
            for error in model_rsp['errors']:
                messages.error(request, error)
    return redirect('home:signup')
    
def logout(request):

    if request.method == "POST":
        if 'user_id' in request.session:
           request.session.pop('user_id')
           request.session.pop('user')
    request.session['user_status'] = 'logged out'   
    return redirect("home:signup" )
    
def success(request):
    if 'user_id' in request.session: 
        request.session['user_status']  = 'logged in'  
        return redirect('dashboard:home')
    else :
        return redirect('home' )