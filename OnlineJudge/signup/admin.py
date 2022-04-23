from django.contrib import admin
from .models import Problem, Solution, TestCase, Language

admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Solution)
admin.site.register(Language)