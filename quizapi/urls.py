from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from quizapi.views import registrationAPIView,QuestionAPIView,CategoryAPIView,AnswerAPIView,ResultAPIView,AnswerAPIView,ProgressAPIView
app_name = 'quizapi'

urlpatterns = [
    # path('register',registration_view, name='register'),
    path('register/',registrationAPIView.as_view(), name='register'),
    path('log_in/', obtain_auth_token ,name='api_log_in'),
    path('categories/',CategoryAPIView.as_view(),name = 'API_category'),
    path('question/<slug:pk>/',QuestionAPIView.as_view(),name = 'API_question'),
    path('ans/<slug:id>/',AnswerAPIView.as_view(), name= 'APIans'),
    path('progress/',ProgressAPIView.as_view(),name = 'API_progress'),
    path('result/<slug:pk>/',ResultAPIView.as_view(),name = 'API_result'),
    
]
