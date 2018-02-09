"""Configure models to be displayed in admin site"""
from django.contrib import admin
from .models import TestQuestion, TestSuite

admin.site.register(TestQuestion)
admin.site.register(TestSuite)
