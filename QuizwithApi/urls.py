from django.urls import path,URLPattern
from QuizwithApi.views import *

urlpatterns = [
    # ex: /polls/
    path('quizapp',index ,name='quizapp'),
]