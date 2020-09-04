from django.urls import path,URLPattern
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
# from . import views
from .views import IndexView,SignUpView,QuizView,ResultView

urlpatterns = [
    # ex: /polls/
    path('account/login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
    path('', IndexView.as_view(), name='index'),
    path('signup/',SignUpView.as_view(), name='signup'),
    path('questions/<slug:pk>/',QuizView.as_view(),name='questions'),
    path('result',ResultView.as_view(),name='result')
    #url for funtion based views
    # path('',views.index, name='index'),
    # path('signup/',views.signup, name='signup'),
    # path('questions/<slug:cat_id>/',views.quiz,name='questions'),
    # path('result',views.result,name='result')

]
    