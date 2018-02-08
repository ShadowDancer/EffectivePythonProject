from django.urls import  include, path
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('tests/<int:testId>/manage', views.manageTest, name='manageTest'),
    path('tests/<int:testId>/questions/<int:questionId>', views.testQuestion, name='testQuestion'),
    path('tests/<int:testId>/questions/<int:questionId>/submit', views.submitQuestion, name='submitQuestion'),
    path(r'', views.index, name='index'),
]