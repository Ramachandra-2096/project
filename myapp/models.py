# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255) 
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    comp_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event_photo = models.ImageField(upload_to='static/course_photos/') 
    date = models.DateTimeField()
    def __str__(self):
        return self.event_name

class PurchasedTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=280)
    is_valid = models.BooleanField(default=True)
    def __str__(self):
        return self.event.event_name
    
    
class Gallery(models.Model):
    year =models.CharField(max_length=255)
    photo = models.ImageField(upload_to='static/image/') 
    
class event_registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    usn = models.CharField(max_length=255)
    payment_photo = models.ImageField(upload_to='static/payment/')
    payment_status = models.BooleanField(default=False)
