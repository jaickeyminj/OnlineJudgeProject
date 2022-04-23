from django.db import models
from django.utils import timezone

# Create your models here.
class Problem(models.Model):
    problem_id = models.CharField(max_length=20,primary_key=True)
    problem_title= models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    difficulty = models.CharField(max_length=10,default='Easy')

    def __str__(self):
        return f"{self.problem_id} -> {self.problem_title}"

class Solution(models.Model):
    code = models.CharField(max_length=3000)
    problem_id = models.OneToOneField(Problem, verbose_name=('problem_id'),primary_key=True,on_delete=models.CASCADE)
    verdict = models.CharField(max_length=20)
    time = models.DateField(default=timezone.now)
    def __str__(self):
        return f"{self.problem_id} -> {self.verdict}"

class TestCase(models.Model):
    input = models.CharField(max_length=200)
    output = models.CharField(max_length=200)
    problem_id = models.OneToOneField(Problem, verbose_name=('problem_id'),primary_key=True,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.problem_id}"

class Language(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name} "