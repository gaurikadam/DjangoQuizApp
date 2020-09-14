from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate
from .forms import SignUpForm
import logging

from django.http import JsonResponse
from .models import Question,Category,Progress,Answer,Result, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils import timezone
import json
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.views import generic
from django.utils.decorators import method_decorator
from django.views import View
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 

from django.template.loader import get_template 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 


class IndexView(LoginRequiredMixin,View):
     login_url = '/account/login/'
     template_name = 'quiz/index.html'

     def get(self,request):

          # Loads category and total marks scored
          category_object = Category.objects.order_by('id')
          user = request.user
          progress = Progress.objects.filter(user=user)
          
          score_dict = {}
          if progress is not None:
               for p in progress:
               
                    quiz_category_id = p.category.id
                    score_dict[quiz_category_id] = [p.marks,p.total]
               return render(request,self.template_name,{'cat':category_object,'dict':score_dict}) 

               
          else:          
               return render(request,self.template_name,{'cat':category_object}) 


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user) 
            messages.success(request, ('Your account have been confirmed.'))

            return redirect('/account/login/')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/')


class SignUpView(View):
     # login_url = '/account/login/'
   
     form_class = SignUpForm
     intial ={}
     template_name = 'registration/sign_up.html'

     def get(self, request, *args, **kwargs):
          form = self.form_class()
          return render(request,self.template_name,{'form':form})

     
     def post(self, request, *args, **kwargs):
          form = self.form_class(request.POST)
          if form.is_valid():
               user = form.save()
               user.is_active = False # Deactivate account till it is confirmed
               user.save()
               current_site = get_current_site(request)
               subject = 'Activate Your MySite Account'
               message = render_to_string('registration/account_active_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
               user.email_user(subject, message)
               logger.info(message)
               messages.success(request, ('Please Confirm your email to complete registration.'))
               logger.info('check link in console')
                       
               return redirect('/account/login/')

          return render(request,self.template_name,{'form':form})


class QuizView(LoginRequiredMixin,View):
     login_url = '/account/login/'
     template_name = 'quiz/question_submit_form.html'
     
     def get(self,request,*args, **kwargs):
          pk = self.kwargs.get('pk')
          user = request.user
          
          category_objects = get_object_or_404(Category,pk =pk)
          questions = Question.objects.filter(category = category_objects)
         
          for question in questions.all():
               try:
                    question_in_result = Result.objects.get(user=user,question=question)
                    
                   
                    continue
               except Result.DoesNotExist:

                    answers = Answer.objects.filter(question=question)
                    return render(request,self.template_name,{'answer':answers,'question':question})

          return render(request,self.template_name,{'complete':True,'Current_category_id':pk})          
     
    
     def post(self, request, *args, **kwargs):
          pk = self.kwargs.get('pk')
          user = request.user
          post_data_list = list(request.POST.items())
          user = request.user
          question_in_request = post_data_list[1][0]
          selected_answer_in_request=post_data_list[1][1]
          question = get_object_or_404(Question,id=question_in_request)
          selected_answer = get_object_or_404(Answer,id=selected_answer_in_request)
          select_answer_in_form =selected_answer.answer
          correct_answer_id = ''
          answers = Answer.objects.filter(question=question)
          true_answer = ''
          answer = answers.filter(is_correct=True)
          for ans in answer.all():
               true_answer =ans.answer
          correct_answer_id = ans.id
          if str(correct_answer_id) == str(post_data_list[1][1]):
               result = Result.objects.create(user=user,
                                        question=question,
                                        # correct_answer=true_answer,
                                        # selected_answer=select_answer_in_form,
                                    is_correct=True)
               add_to_progress(request,question,True)
               current_category_id =  str(result.question.category.id)
               next_question_url= "/questions/" + current_category_id
               return redirect(next_question_url)
   
          else:
               result = Result.objects.create(user=user,
                                        question=question,
                                        # correct_answer=true_answer,
                                        # selected_answer=select_answer_in_form,
                                        is_correct=False)
               add_to_progress(request,question,False)
               current_category_id =  str(result.question.category.id)
               next_question_url= "/questions/" + current_category_id
               return redirect(next_question_url)

     
     
     
def add_to_progress(request,question,correctness):

    user = request.user
    category = question.category
    increase_mark = 0
    total_questions = Question.objects.filter(category=category).count()
    if correctness:
          increase_mark = 1
     
    if Progress.DoesNotExist:
          progress = Progress.objects.create(user=user,category=category,marks=increase_mark,total=total_questions)

    else:
          progress = Progress.objects.filter(user=user,category=category)
          progress.marks += increase_mark
          progress.save()
          

# @method_decorator(login_required, name='dispatch')
class ResultView(LoginRequiredMixin,View):
     login_url = '/account/login/'
     template_name = 'quiz/result.html'
     
     def get(self,request,*args, **kwargs):
          pk = self.kwargs.get('pk')
          user = request.user
          questions = Result.objects.filter(user=user,question__category__id = pk)
          return render(request,self.template_name,{'Question':questions})

  






