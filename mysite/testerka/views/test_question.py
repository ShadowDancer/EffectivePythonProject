"""View test question"""
from datetime import timedelta, datetime

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.views.decorators.http import require_GET

from ..models import UserTestSuite, TestQuestion
from .question_helper import load_user_test, validate_question

@login_required
@require_GET
def test_question(request, test_id, question_id):
    """View single test question"""
    now = datetime.now()
    user_test = load_user_test(request, test_id)
    if user_test is not UserTestSuite:
        return user_test

    question = validate_question(request, test_id, user_test, question_id)
    if question is not TestQuestion:
        return question

    question.id = question_id
    user_test.testSuite.timeLeft = user_test.testSuite.dateEnd - now
    user_test.testSuite.timeLeft = user_test.testSuite.timeLeft - \
        timedelta(microseconds=user_test.testSuite.timeLeft.microseconds)

    template = loader.get_template('test/question.html')
    context = {
        'test': user_test.testSuite,
        'question': question
    }

    return HttpResponse(template.render(context, request))
