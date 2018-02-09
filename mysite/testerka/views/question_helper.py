"""Helper functions for views servicing request for single question"""
from datetime import datetime

from django.shortcuts import redirect

from .view_test_helper import test_forbiden, test_not_found, test_finished
from ..models import TestSuite, UserTestSuite, TestQuestion

def load_test(request, test_id):
    """Loads test by id
    returns test or HttpResponse on error"""
    test_query = TestSuite.objects.filter(id=test_id)
    if len(test_query) != 1:
        return test_not_found(request)
    test = test_query[0]
    test.dateStart = test.dateStart.replace(tzinfo=None)
    test.dateEnd = test.dateEnd.replace(tzinfo=None)
    return test

def load_user_test(request, test_id):
    """Loads user test by given test id checking if user can access this test
    returns UserTest or HttpResponse on error"""
    test = load_test(request, test_id)
    if test is not TestSuite:
        return test

    # check if test is not expired
    now = datetime.now().replace(tzinfo=None)
    if not (now >= test.dateStart and now <= test.dateEnd):
        return test_forbiden(request)

    user_test_query = UserTestSuite.objects.filter(testSuite=test, user=request.user)
    user_test = None
    if user_test_query:
        user_test = user_test_query[0]
    else:
        # nie ma informacji o teście dla użytkownika, tworzymy
        user_test = UserTestSuite()
        user_test.testSuite = test
        user_test.user = request.user
        user_test.save()
    if user_test.finished:
        return test_finished(request)
    return user_test

def validate_question(request, test_id, user_test, question_id):
    """Loads question with given is for user test
    return TestQuestion or HttpResponse on error"""
    if question_id != user_test.currentQuestion:
        # attempt to view invalid question
        return redirect(f'/tests/{test_id}/questions/{user_test.currentQuestion}')

    # wczytaj pytania
    questions = TestQuestion.objects.filter(testSuite=user_test.testSuite)
    if question_id - 1 >= len(questions):
        return test_not_found(request)

    return questions[question_id - 1]
