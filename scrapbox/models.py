from django.db import models

from django.contrib.auth.models import User

from datetime import datetime

from django.utils import timezone

from django.db.models.signals import post_save 

# Create your models here.

class Scrapbox(models.Model):

    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    price=models.IntegerField()
    location=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="images",null=True)
    phone_no=models.CharField(max_length=200,null=True)
   

    def __str__(self):
            
        return self.name
    
    #then go to form.py
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    email=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    profile_pic=models.ImageField(upload_to="profilepics",null=True,blank=True)
    

    def __str__(self):
        return self.user.username
    
class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userpost")
    title=models.CharField(max_length=200)
    post_image=models.ImageField(upload_to="posters",null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title

class Comments(models.Model):
    user=models.ForeignKey(User,related_name="comment",on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Posts,related_name="post_comments",on_delete=models.CASCADE)


def create_profile(sender,created,instance,**kwargs):
        if created:
            UserProfile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)
