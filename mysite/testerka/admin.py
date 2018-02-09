"""Configure models to be displayed in admin site"""
from django.contrib import admin
from .models import TestQuestion, TestSuite


class TestQuestionInline(admin.StackedInline):
    """"Allows edition of questions in test suite panel"""
    model = TestQuestion
    extra = 0
    min_num = 1


class TestSuiteAdmin(admin.ModelAdmin):
    """Configures tests suite admin panel"""
    model = TestSuite
    inlines = [TestQuestionInline, ]

admin.site.register(TestSuite, TestSuiteAdmin)
