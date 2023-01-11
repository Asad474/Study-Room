from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True) 
    bio=models.TextField(null=True)
    avatar=models.ImageField(null=True,default="avatar.svg")

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]


class Topic(models.Model):
    name=models.CharField(unique=True,max_length=50)
    def __str__(self):
        return self.name


class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    name=models.TextField(blank=True,unique=True,max_length=100)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-updated','-created']

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    room=models.ForeignKey(Room,on_delete=models.SET_NULL,null=True)
    body=models.TextField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated','-created']  

    def __str__(self):
        return self.body[:25]