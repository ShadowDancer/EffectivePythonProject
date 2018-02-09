"""Reports answers of all test to administration"""
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import loader
from django.views.decorators.http import require_GET

from ..models import UserTestSuite, UserTestQuestion
from .question_helper import load_test


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_GET
def manage_test(request, test_id):
    """Displays all answers for test submitted by users"""

    test = load_test(request, test_id)
    if test is not UserTestSuite:
        return test

    user_test_suites = UserTestSuite.objects.filter(testSuite=test)

    for user_test in user_test_suites:
        user_test.questions = UserTestQuestion.objects.filter(
            userTestSuite=user_test)

    template = loader.get_template('test/manage.html')
    context = {
        'test': test,
        'userTests': user_test_suites
    }

    return HttpResponse(template.render(context, request))
