from django.urls import path,URLPattern
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('questions/<slug:cat_id>/',views.quiz,name='questions')
    # path('result/',views.quiz,name='result')

    

    # ex: /polls/5/
    #
]
# reset/<uidb64>/<token>/'
# activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$