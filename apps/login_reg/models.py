from __future__ import unicode_literals
from django.db import models
import re  # import python regex module
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
DATE_REGEX = re.compile(r'^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$')
class UserManager(models.Manager):
    
        def registration(self, data):
            errors = []
            
            if len(data['first_name']) < 2:
                errors.append("first name is empty or needs more 2 chars")
            if len(data['last_name']) < 2:
                errors.append("last name is empty  or needs more 2 chars")
            if len(data['email']) < 1:
                errors.append(" email is empty")
            if not EMAIL_REGEX.match(data['email']):
                errors.append(" email is not valid")    
            if not DATE_REGEX.match(data['date_hired']):
                errors.append(" date is not valid")                    
            if len(data['password']) < 8:
                errors.append("password is empty  or needs more 8 chars")                 
            if len(data['confirm_ps']) < 8:
                errors.append("confirm password is empty  or needs more 8 chars")
                
            if data['confirm_ps'] != data['password'] :
                errors.append("password and confirm password are not equal")
            if len(errors) == 0:
                user = self.filter(email=data['email'])            
                if user :
                    errors.append("user alraedy exist")
                    
            msgRsp = {}
            
            if len(errors) > 0:
                msgRsp['status'] = False
                msgRsp['errors'] = errors
            else :
                hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
                user = self.create(first_name=data['first_name'],
                            last_name=data['last_name'],
                            email=data['email'],
                            password=hashed_password)
                msgRsp['status'] = True
                msgRsp['user'] = user
                
            return msgRsp    
            
        def login(self, data):
            
            msgRsp = {}            
            errors = []
            
            if len(data['email']) < 1:
                errors.append(" email is empty")
            if not EMAIL_REGEX.match(data['email']):
                errors.append(" email is not valid")
            if len(data['password']) < 8:
                errors.append("password is empty  or needs more 8 chars") 
                
            if len(errors) == 0:
                user = self.filter(email=data['email'])            
                if user :
                    if bcrypt.checkpw(data['password'].encode(), user[0].password.encode()):
                        msgRsp['status'] = True
                        msgRsp['user'] = user[0]
                    else :
                        errors.append("Invalid password try again")
                        msgRsp['status'] = False
                        msgRsp['errors'] = errors
                else :  
                    errors.append("Invalid user try again")
                    msgRsp['status'] = False
                    msgRsp['errors'] = errors
            else :
                msgRsp['status'] = False
                msgRsp['errors'] = errors
            return msgRsp

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=34)
    last_name = models.CharField(max_length=34)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=256)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()