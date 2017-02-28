from django.shortcuts import render ,redirect
from models import Appointment
from django.contrib import messages
from datetime import datetime

# Create your views here.
def index(request):
    
    try:
        context = {
                'first_name': request.session['user'],
                'login_id': request.session['user_id'],
                'status': request.session['user_status'], 
                'task_date':datetime.now(),
                'current_appointments': Appointment.objects.getCurrentTasks(request.session['user_id']),
                'other_appointments':Appointment.objects.getFutureTasks(request.session['user_id'])                
            }        
        
        return render( request, 'main_app/index.html', context)
    except KeyError:
            return redirect('home:signup')         



def add(request):
    
    if request.method == 'POST':
        try:
            context = {
                    'first_name': request.session['user'],
                    'status': request.session['user_status'],                             
                }
                
            print context
            rsp = Appointment.objects.addTask(request.session['user_id'], request.POST)  
            print rsp            
            if rsp['status'] :            
                for error in rsp['errors']:
                    messages.error(request, error)
            return redirect('dashboard:home')
        except KeyError:
                return redirect('home:signup')
                
def showUpdate(request, task_id):
   
    try:
        context = {
                'first_name': request.session['user'],
                'status': request.session['user_status'], 
                'appointment':Appointment.objects.getTask(task_id)
            }        
        
        return render( request, 'main_app/update.html', context)
    except KeyError:
            return redirect('home:signup')

def showDelete(request, task_id):
   
    try:
        context = {
                'first_name': request.session['user'],
                'status': request.session['user_status'], 
                'appointment':Appointment.objects.getTask(task_id)
            }       
        
        return render( request, 'main_app/delete.html', context)
    except KeyError:
            return redirect('home:signup')

            
def update(request, task_id):   
   
   if request.method == 'POST':
        try:
            context = {
                    'first_name': request.session['user'],
                    'status': request.session['user_status'],                             
                }
                
            print context
            rsp = Appointment.objects.updateTask(request.session['user_id'], task_id, request.POST) 
            print rsp            
            if rsp['status'] :            
                for error in rsp['errors']:
                    messages.error(request, error)
            return redirect('dashboard:home')
        except KeyError:
                return redirect('home:signup')
            
def delete(request, task_id):
    
    if request.method == 'POST':
        try:
            context = {
                    'first_name': request.session['user'],
                    'status': request.session['user_status'],                             
                }
            rsp = Appointment.objects.deleteTask(task_id)  
            return redirect('dashboard:home')            
        except KeyError:
            return redirect('home:signup')
