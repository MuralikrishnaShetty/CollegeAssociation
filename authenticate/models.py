from django.db import models
# Create your models here.

class Post(models.Model):
    date= models.DateField()
    time = models.TimeField()
    content = models.TextField()
    fname = models.CharField(max_length = 20)
    lname = models.CharField(max_length = 20)
    image=models.ImageField(upload_to="image/", default='default_image.jpg')
    


class Finance(models.Model):
    date= models.DateField()
    time = models.TimeField()
    event = models.CharField(max_length=20)
    cost = models.BigIntegerField()
    fname = models.CharField(max_length = 20)
    lname = models.CharField(max_length = 20)


