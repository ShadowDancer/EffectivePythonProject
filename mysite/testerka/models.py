from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings


# Create your models here.

class TestSuite(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, verbose_name="Nazwa", default="Nazwa testu")
    dateStart = models.DateTimeField(verbose_name="Data rozpoczęcia", default=datetime.now)
    dateEnd = models.DateTimeField(verbose_name="Data zakończenia", default=datetime.now)

    def __str__(self):
        return str(self.dateStart) + ' ' + self.name

class TestQuestion(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, verbose_name="Nazwa", default="Nazwa pytania")
    questionText = models.TextField(verbose_name="Pytanie", default="Treść pytania")
    testsText = models.TextField(verbose_name="Testy", default="")
    testSuite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        order_with_respect_to = 'testSuite'
        
class UserTestSuite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    testSuite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    currentQuestion = models.IntegerField(default=1)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return str(self.dateStart) + ' ' + self.name

class UserTestQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    userTestSuite = models.ForeignKey(UserTestSuite, on_delete=models.CASCADE)
    testQuestion = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    answer = models.TextField(default="")
