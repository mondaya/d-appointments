from __future__ import unicode_literals

from django.db import models
from ..login_reg.models import User
from datetime import datetime
import re  # import python regex module
# Create your models here. 

DATE_REGEX = re.compile(r'^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$')
TIME_REGEX = re.compile(r'^[0-9]{2}:[0-9]{2}$')
   
   
class AppointmentManager(models.Manager):
       
    def validateTaskData(self, data):
        print "doing vlaidation"
        errors = []

        if len(data['task']) < 1:
            errors.append("Task info is empty")
        if len(data['status']) < 1:
            errors.append("Missing status")
        if len(data['date']) < 1:
            errors.append(" date is empty")               
        if not DATE_REGEX.match(data['date']):
            errors.append("date is not valid")                    
        if len(data['time']) < 1:
            errors.append("time is empty")                 
        if not TIME_REGEX.match(data['time']):
            errors.append("time is not valid") 
            
        if len(errors) == 0:    
            strdatetime =  data['date'] + " " + data['time']
            datetime_object = datetime.strptime(strdatetime, '%m/%d/%Y %H:%M')

            if datetime_object < datetime.now():
                errors.append("date and time is not of the current of future date")
            
        if len(errors):
            return {'status':True, 'errors':errors}
        else:
            return {'status':False, 'datetime':datetime_object}   
            
    def getCurrentTasks(self, user_id):
        today = datetime.now()
        tasks =  self.filter(user__id=user_id, 
        taskdatetime__year=today.year,
        taskdatetime__month=today.month, 
        taskdatetime__day=today.day).order_by('taskdatetime')
        return tasks
       
    def getFutureTasks(self, user_id):       
        today = datetime.now()
        print today
        tasks =  self.exclude(taskdatetime__date__lte=today.date(),                            
                            ).filter(user__id=user_id,).order_by('taskdatetime')
        return tasks
        
    def getTask(self, task_id):             
        usrtask = self.get(id=task_id)
        return usrtask
        
    def deleteTask(self, task_id):
        rsp = {}
        rsp['status'] = False
        try :    
            usrtask = self.get(id=task_id)
            usrtask.delete()
        except DoesNotExist:
            rsp['status'] = True
            rsp['errors'] = ["Appointment matching query does not exist"]
        return rsp 
        
        
        
    def addTask(self,user_id, postData):
    
        rsp = self.validateTaskData(postData)
        print "done with validation"
        print rsp
        if rsp['status'] : # if validation errors
            return rsp
        else :
            try  :
                req_datetime = rsp['datetime'] 
                user = User.objects.get(id=user_id)                
                task = self.create(task=postData['task'], user=user, taskdatetime=req_datetime,  status=postData['status'])
                print task
            except:
                rsp['status'] = True
                rsp['errors'] = ["Duplicate error."]
            return rsp

    def updateTask(self,user_id, task_id, postData):
    
        rsp = self.validateTaskData(postData)
        if rsp['status'] : # if validation errors
            return rsp
        else :
            req_datetime = rsp['datetime'] 
            user = User.objects.get(id=user_id) 
            try :            
                usrtask = self.get(id=task_id)
                usrtask.task=postData['task']
                usrtask.user=user 
                usrtask.taskdatetime=req_datetime
                usrtask.status=postData['status'] 
                usrtask.save()
            except :
                rsp['status'] = True
                rsp['errors'] = ["Either the entry or blog doesn't exist or Duplicate error."]
            return rsp        
    
                
class Appointment(models.Model):
    
    task=models.CharField(max_length=3000)  
    user=models.ForeignKey(User, related_name='task_added_by')
    taskdatetime=models.DateTimeField(auto_now=False, auto_now_add=False)
    status=models.CharField(max_length=30) 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)    
    objects=AppointmentManager()
    
    class Meta:
        unique_together = (("user", "taskdatetime"),)
    
