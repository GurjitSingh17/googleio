from django.db import models

# Create your models here.

class link(models.Model):
    url = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    true_url = models.CharField(max_length=200,default="not found")

class vid_link(models.Model):
    vid_id = models.CharField(max_length=100)

