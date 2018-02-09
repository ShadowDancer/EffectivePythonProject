"""Url configuration for testerka app"""

from django.urls import  include, path
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('tests/<int:test_id>/manage', views.manage_test, name='manage_test'),
    path('tests/<int:test_id>/questions/<int:question_id>',
         views.test_question, name='test_question'),
    path('tests/<int:test_id>/questions/<int:question_id>/submit',
         views.submit_question, name='submit_question'),
    path(r'', views.index, name='index'),
]
