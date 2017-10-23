from __future__ import unicode_literals
import re
from django.db import models

# Create your models here.


EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def validate(self,post_data):
        errors={}
        for field,value in post_data.iteritems():
            if len(value)<1:
                errors[field]="{} field is required".format(field.replace('_',''))
            if field == "first_name" or field =="last_name":
                if not field in errors and len(value) < 3:
                    errors[field]="{} field must be at least 3 characters".format(field.replace('_',''))
        if not "email" in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email']="Invalid Email"
        else:
            if len(self.filter(email=post_data['email']))> 1:
                errors['email']= "Email is already in use"
        return errors




class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)       # needs add
    updated_at = models.DateTimeField(auto_now=True)           # does not need add
    objects = UserManager()
    def __repr__(self):
        return "first:: {} last:: {} ".format(self.first_name,self.last_name)

