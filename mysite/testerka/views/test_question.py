"""View test question"""
from datetime import timedelta, datetime

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.views.decorators.http import require_GET

from ..models import UserTestSuite
from .question_helper import load_user_test, validate_question


@login_required
@require_GET
def test_question(request, test_id, question_id):
    """View single test question"""
    now = datetime.now().replace(tzinfo=None)
    user_test = load_user_test(request, test_id)
    if isinstance(user_test, HttpResponse):
        return user_test

    question_result = validate_question(request, test_id, user_test, question_id)
    if  isinstance(question_result, HttpResponse):
        return question_result
    question = question_result[0]

    question.id = question_id
    time_left = user_test.testSuite.dateEnd.replace(tzinfo=None) - now
    time_left = time_left - timedelta(microseconds=time_left.microseconds)
    user_test.testSuite.timeLeft = time_left

    template = loader.get_template('test/question.html')
    context = {
        'test': user_test.testSuite,
        'question': question
    }

    return HttpResponse(template.render(context, request))
