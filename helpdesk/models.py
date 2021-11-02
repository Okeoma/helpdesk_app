from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime

   
class User(AbstractUser):
    pass
    ACCESS = (
        ('Regular', 'Regular'),
        ('Standard', 'Standard'),
        ('Admin', 'Admin')
    )    
    access = models.CharField(max_length=15, choices=ACCESS, verbose_name="access", default="Regular") 
    role = models.CharField(max_length=60) 
    location = models.CharField(max_length=120, blank=True)  
    
class Customer(models.Model): 
    customer =  models.CharField(max_length=30, unique=True) 
    firstname =  models.CharField(max_length=30)  
    lastname =  models.CharField(max_length=30)
    email =  models.CharField(max_length=30) 
    phone_no = models.CharField(max_length=20)
    company = models.CharField(max_length=30)
    location = models.CharField(max_length=120, blank=True)   
    
    def __str__(self):
        return f"{self.customer}"
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trouble_ticket')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='client')
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=500, default=None)
    comments = models.ManyToManyField('Comment', blank=True, related_name='comments_ticket')
    date = models.DateTimeField(default=datetime.datetime.now)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: {self.user}, title: {self.title}, customer: {self.customer}"
		
class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s' % (self.user, self.date)

class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_profile')
    image = models.ImageField(upload_to='images', null=True)
	
    def __str__(self):
        return f"{self.id}: {self.user}"	
        
class Dynamics(models.Model):  
    name = models.CharField(max_length=150)  
    image = models.ImageField(upload_to='images', blank=True, null=True)
	
    def __str__(self):
        return f"{self.id}: {self.name}"		
		
class Ticketrank(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = (('ticket', 'user'),)
    def __str__(self):
        return f"{self.ticket} : {self.user}"
        

class Senior(models.Model):
    senior = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senior', default=None)
    junior = models.ForeignKey(User, on_delete=models.CASCADE, related_name='junior', default=None)

    class Meta:
        unique_together = (('senior', 'junior'),)
    def __str__(self):
            return f"{self.senior} : {self.junior}"

