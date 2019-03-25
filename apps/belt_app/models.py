from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[!$?])(?=.*[a-z])(?=.*[A-Z]).{8}$')


class registration_manager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address!"
        users = User.objects.filter(email = postData["email"])
        if users.count() > 0:
            errors['email'] = "Email already taken"
        # if not PASSWORD_REGEX.match(postData['password']):
        #     errors['password'] = "Invalid password"
        if len(postData["password"]) < 8:
            errors['password'] = "Passwords must be 8 characters long"
        if postData["password"] != postData["password_confirm"]:
            errors["pw_confirm"] = "Passwords must match!"
        return errors

    def login_validator(self,postData):
        errors = {}

        users = User.objects.filter(email = postData["email"])
        if users.count() == 0:
            errors["login"] = "Invalid login"
            

            return errors
        else:
            user = User.objects.get(email=postData["email"])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()) == False:
                errors["login"] = "Invalid login"
                
        return errors

    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Job title should be at least 3 characters long"
        if len(postData['description']) < 3:
            errors['description'] = "Job description must be at least 3 characters long"
        if len(postData['location']) < 3:
            errors['location'] = "Location should be at least 3 characters long"

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = registration_manager()



class Job(models.Model):
    title = models.CharField(max_length=45)
    desc = models.TextField()
    location = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='jobs_created')
    workers = models.ManyToManyField(User, related_name='current_jobs')
 

class Category(models.Model):
    category = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(Job, related_name="categories")


















