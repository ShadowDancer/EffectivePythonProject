from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from datetime import timedelta, datetime
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ..models import TestSuite, UserTestSuite, TestQuestion, UserTestQuestion
# Create your views here.

# wyświetla stronę testu
@login_required
@require_POST
def submitQuestion(request, testId, questionId):
    testQuery = TestSuite.objects.filter(id=testId)
    #nie znaleziono testu
    if len(testQuery) != 1:
        return testNotFound(request)
    test = testQuery[0]
    test.dateStart = test.dateStart.replace(tzinfo=None)
    test.dateEnd = test.dateEnd.replace(tzinfo=None)
    now = datetime.now().replace(tzinfo=None)
    user = request.user
    # upłynął czas testu, lub czas nie rozpoczęty
    if not (now >= test.dateStart and now <= test.dateEnd):
        return testForbidden(request)
        
    userTestQuery = UserTestSuite.objects.filter(testSuite=test,user=user)
    userTest = None
    if len(userTestQuery) > 0:
        userTest = userTestQuery[0]
    else:
        #nie ma informacji o teście dla użytkownika, tworzymy
        userTest = UserTestSuite()
        userTest.testSuite=test
        userTest.user=user
        userTest.save()
    if userTest.finished:
        # test zakończony
        return testFinished(request)
    if questionId != userTest.currentQuestion:
        # osoba próbuje podejreć inne pytanie
        return redirect(f'/tests/{test.id}/questions/{userTest.currentQuestion}')

    # wczytaj pytania
    questions = TestQuestion.objects.filter(testSuite=test)
    if questionId -1 >= len(questions):
        return testNotFound(request)

    question = questions[questionId - 1]
    
    userQuestion = UserTestQuestion()
    userQuestion.testQuestion = question
    userQuestion.userTestSuite = userTest
    print(request.POST['answer'])
    userQuestion.answer = request.POST['answer']
    userQuestion.save()

    userTest.currentQuestion = userTest.currentQuestion + 1
    if userTest.currentQuestion > len(questions):
        userTest.finished = True
    userTest.save()
    
    return redirect(f'/tests/{test.id}/questions/{userTest.currentQuestion}')

def testNotFound(request):
    return HttpResponse(loader.get_template('test/notfound.html').render(None, request))

def testForbidden(request):
    return HttpResponse(loader.get_template('test/forbidden.html').render(None, request))

def testFinished(request):
    return HttpResponse(loader.get_template('test/finished.html').render(None, request))