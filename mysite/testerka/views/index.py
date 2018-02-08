from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from datetime import datetime

from ..models import TestSuite, UserTestSuite


# pobiera listę testów i renderuje
@login_required
def index(request):
    tests = getTests(request.user)
    template = loader.get_template('test/index.html')
    context = {
        'tests': tests,
    }
    return HttpResponse(template.render(context, request))

def getTests(user):
    now = datetime.now().replace(tzinfo=None)
    tests = TestSuite.objects.order_by('-dateStart')
    userTests = UserTestSuite.objects.filter(user=user)
    for test in tests:
        test.dateStart = test.dateStart.replace(tzinfo=None)
        test.dateEnd = test.dateEnd.replace(tzinfo=None)
        test.awaiting = now < test.dateStart
        test.expired = now > test.dateEnd
        test.finished = False
        test.currentQuestion = 1
        for userTest in userTests:
            if userTest.id == test.id:
                if userTest.finished:
                    test.finished = True
                test.currentQuestion = userTest.currentQuestion
        test.available = not test.awaiting and not test.expired and not test.finished
    return tests