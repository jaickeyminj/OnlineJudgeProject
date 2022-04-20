from django.db import models

# Create your models here.
class Problem(models.Model):
    problem_id = models.CharField(max_length=20)
    problem_title= models.CharField(max_length=100)
    description = models.CharField(max_length=2000)