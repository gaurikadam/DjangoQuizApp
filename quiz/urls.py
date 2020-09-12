from django.urls import path,URLPattern
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
# from . import views
from .views import IndexView,SignUpView,QuizView,ResultView,ActivateAccount

urlpatterns = [
    # ex: /polls/
    path('account/login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
    path('', IndexView.as_view(), name='index'),
    path('signup/',SignUpView.as_view(), name='signup'),
    path('questions/<slug:pk>/',QuizView.as_view(),name='questions'),
    path('result/<slug:pk>/',ResultView.as_view(),name='result'),
    path('account/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password-change-done.html')),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='registration/password-change.html',success_url = '/account/password_change/done/'), name='change_password'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    #reset
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='registration/password-reset.html'), name='password-reset'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('account/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-done.html'), name='password-reset-done'),
    path('account/confirm/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-token.html'), name='password-reset-confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'), name='password-reset-complete'),

]

    #url for funtion based views
    # path('',views.index, name='index'),
    # path('signup/',views.signup, name='signup'),
    # path('questions/<slug:cat_id>/',views.quiz,name='questions'),
    # path('result',views.result,name='result')