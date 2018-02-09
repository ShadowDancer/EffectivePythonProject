"""Views of main page containing list of tests which can be executed"""
from datetime import datetime

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader

from ..models import TestSuite, UserTestSuite


@login_required
def index(request):
    """Main page with list of tests"""
    tests = _get_tests(request.user)
    template = loader.get_template('test/index.html')
    context = {
        'tests': tests,
    }
    return HttpResponse(template.render(context, request))


def _get_tests(user):
    """Loads all tests from database adds additional metadata"""
    now = datetime.now().replace(tzinfo=None)
    tests = TestSuite.objects.order_by('-dateStart')
    user_tests = UserTestSuite.objects.filter(user=user)
    for test in tests:
        test.dateStart = test.dateStart.replace(tzinfo=None)
        test.dateEnd = test.dateEnd.replace(tzinfo=None)
        test.awaiting = now < test.dateStart
        test.expired = now > test.dateEnd
        test.finished = False
        test.currentQuestion = 1
        for user_test in user_tests:
            if user_test.id == test.id:
                if user_test.finished:
                    test.finished = True
                test.currentQuestion = user_test.currentQuestion
        test.available = not test.awaiting and not test.expired and not test.finished
    return tests
