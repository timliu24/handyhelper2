from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must enter an valid email."
        users_with_email = User.objects.filter(email=postData['email'])
        if len(users_with_email) >= 1:
            errors['email'] = "Email already registered."
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['match'] = "Password does not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Title must consist of at least 3 characters."
        if len(postData['description']) < 3:
            errors['description'] = "Description must consist of at least 3 characters."
        if len(postData['location']) < 3:
            errors['location'] = "Location must consist of at least 3 characters."
        return errors

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # category = models.BooleanField()
    creator = models.ForeignKey(User, related_name="has_posted_job", on_delete=models.CASCADE)
    added_by = models.ManyToManyField(User, related_name="added_jobs")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = JobManager()