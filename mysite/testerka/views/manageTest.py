from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import loader
from datetime import timedelta, datetime
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from ..models import TestSuite, UserTestSuite, TestQuestion, UserTestQuestion
# Create your views here.

# wyświetla stronę testu
@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_GET
def manageTest(request, testId):
    testQuery = TestSuite.objects.filter(id=testId)
    #nie znaleziono testu
    if len(testQuery) != 1:
        return testNotFound(request)
    test = testQuery[0]
    test.dateStart = test.dateStart.replace(tzinfo=None)
    test.dateEnd = test.dateEnd.replace(tzinfo=None)
    now = datetime.now().replace(tzinfo=None)
    user = request.user
        
    userTestSuites = UserTestSuite.objects.filter(testSuite=test)

    for userTest in userTestSuites:
        userTest.questions = UserTestQuestion.objects.filter(userTestSuite = userTest)

    template = loader.get_template('test/manage.html')
    context = {
        'test': test,
        'userTests': userTestSuites
    }

    return HttpResponse(template.render(context, request))

def testNotFound(request):
    return HttpResponse(loader.get_template('test/notfound.html').render(None, request))
