"""Defines helper functions for common error views"""
from django.http import HttpResponse
from django.template import loader

def test_not_found(request):
    """Suite does not exists"""
    return HttpResponse(loader.get_template('test/notfound.html').render(None, request))

def test_forbiden(request):
    """User cannot access suite because it has not started yet or it is already finished"""
    return HttpResponse(loader.get_template('test/forbidden.html').render(None, request))

def test_finished(request):
    """User already finished this suite"""
    return HttpResponse(loader.get_template('test/finished.html').render(None, request))
