from django.db import models

# Create your models here.

class Welfare(models.Model):
    domain=models.CharField(max_length=15,default='')
    title=models.CharField(max_length=150)
    description=models.TextField()
    link=models.TextField()

    def _str_(self):
        return self.title


