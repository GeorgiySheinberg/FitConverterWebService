from django.db import models


# Create your models here.
class MyFiles(models.Model):
    text = models.CharField(max_length=100)
    file = models.FileField(upload_to='upldfile/')
