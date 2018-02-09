"""Handles from posted when user submitted answer"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from ..models import UserTestQuestion
from .question_helper import load_user_test, validate_question


@login_required
@require_POST
def submit_question(request, test_id, question_id):
    """Handles from posted when user submitted answer
    test_id: identifier of current test
    question_id: identifier of answered question"""

    result = load_user_test(request, test_id)
    if isinstance(result, HttpResponse):
        return result
    user_test = result

    question_result = validate_question(
        request, test_id, user_test, question_id)
    if isinstance(question_result, HttpResponse):
        return question_result
    question, number_of_questions = question_result

    user_question = UserTestQuestion()
    user_question.testQuestion = question
    user_question.userTestSuite = user_test
    user_question.answer = request.POST['answer']
    user_question.save()

    user_test.currentQuestion = user_test.currentQuestion + 1
    print('Aktualne pytanie: ', user_test.currentQuestion, ' ilosc pytan: ', number_of_questions)
    if user_test.currentQuestion > number_of_questions:
        user_test.finished = True
    user_test.save()

    return redirect(f'/tests/{test_id}/questions/{user_test.currentQuestion}')
