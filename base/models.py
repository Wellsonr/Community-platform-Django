from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(default= ("This is my bio, haven't updated yet :)"))

    avatar = models.ImageField(null=True, default="avatar.svg") 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
# Create your models here.
# models.ForeignKey are the methods that use to make a !!ONE TO MANY AND MANY TO ONE!! relationship

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) :
        return self.name

class Room(models.Model): 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) # auto_now take a snapshot of time when we saved this
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add only take a snapshot when we first saves this, when we save this multiples time this value never be change
    
    class Meta() :
        ordering = ['-updated', '-created']
    def __str__ (self) :
        return self.name



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)
    class Meta() :
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.body[:50]