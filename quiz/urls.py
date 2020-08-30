from django.urls import path,URLPattern
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('questions/<slug:cat_id>/',views.quiz,name='questions'),
    path('result',views.result,name='result')

]
