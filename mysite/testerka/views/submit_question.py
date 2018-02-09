"""Handles from posted when user submitted answer"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ..models import UserTestSuite, TestQuestion, UserTestQuestion
from .question_helper import load_user_test, validate_question


@login_required
@require_POST
def submit_question(request, test_id, question_id):
    """Handles from posted when user submitted answer
    test_id: identifier of current test
    question_id: identifier of answered question"""

    result = load_user_test(request, test_id)
    if result is not UserTestSuite:
        return result
    user_test = result

    question = validate_question(request, test_id, user_test, question_id)
    if question is not TestQuestion:
        return question

    user_question = UserTestQuestion()
    user_question.testQuestion = question
    user_question.userTestSuite = user_test
    user_question.answer = request.POST['answer']
    user_question.save()

    user_test.currentQuestion = user_test.currentQuestion + 1
    if user_test.currentQuestion > len(user_test.testSuite.questions):
        user_test.finished = True
    user_test.save()

    return redirect(f'/tests/{test_id}/questions/{user_test.currentQuestion}')
