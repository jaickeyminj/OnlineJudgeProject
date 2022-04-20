from django.contrib import admin
from .models import Problem, Solution, TestCase

admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Solution)