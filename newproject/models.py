from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UploadImage(models.Model):
    image = models.ImageField(upload_to='images')

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=10)
    DOB = models.DateField()
    address = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profilepic',null=True)

class UserBlog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    blog_data = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True)