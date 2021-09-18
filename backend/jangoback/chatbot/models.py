from django.db import models

# Create your models here.
class Welfare(models.Model):
    domain=models.CharField(max_length=15)
    location=models.CharField(max_length=30)
    location_detail=models.CharField(max_length=30)
    title=models.CharField(max_length=100)
    description=models.TextField()
    link=models.TextField()
