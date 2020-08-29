from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate
from .forms import SignUpForm
from .models import Question,Category,Progress,Answer,Result
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils import timezone
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 

from django.template.loader import get_template 
# Create your views here.
@login_required(login_url='/account/login/')
def index(request):
     # //cat = Category.objects.order_by(id)
     catv = Category.objects.all()
     print(catv)
     # print(cat)
     # user = request.user
     return render(request, 'quiz/index.html',{'cat':catv}) 

def signup(request):
     if request.method == "POST":
          form = SignUpForm(request.POST)
          if form.is_valid():
               form.save()
               to_email = form.cleaned_data.get('email')
               username = form.cleaned_data.get('username')
               print(to_email)
               print(username)
               # htmly = get_template('quiz/ Email.html') 
               d = { 'username': username } 
               subject, from_email, to = 'welcome', 'gauribkadam@gmail.com', to_email 
               html_content = "hi this is re"
               msg = EmailMultiAlternatives(subject, html_content, from_email, [to]) 
               # msg.attach_alternative(html_content, "text / html") 
               msg.send()
               # messages.success(request, f'Your account has been created ! You are now')
          return redirect('/account/login/')
     else:
          form = SignUpForm()

     return render(request,'registration/sign_up.html',{"form":form})
     # Ajanta983@@
@login_required(login_url='/account/login/')     
def quiz(request,cat_id):
     cat_obj = get_object_or_404(Category,pk = cat_id)
    
     questions_set = Question.objects.filter(category = cat_obj) # 
     print(questions_set)
     ans = Question.objects.filter(category = cat_obj)
     for question in questions_set:
          # print(question.question)
          # print(type(question.question))
          answers = Answer.objects.filter(question=question)
     # print(Category.objects.all())
     return render(request, 'quiz/questionpage.html',{'question':question,'answer':answers}) 
     # return redirect('/account/login/')
@login_required(login_url='/account/login/')
def progress():
     print("res")
     return redirect('/account/login/')

@login_required(login_url='/account/login/')     
def result():  
     print("res")
     return redirect('/account/login/')
     
