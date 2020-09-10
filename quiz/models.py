from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
# Create your models here.
import uuid 

class Category(models.Model):
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    id = models.AutoField(primary_key=True,editable=False)
    title = models.CharField(max_length=200)

    def __str__(self):
        model_category = str(self.title)
        return model_category

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)



class Question(models.Model):

    id = models.AutoField(primary_key=True,editable=False)
    question = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        model_questions = '{} | {}'.format(str(self.category),str(self.question)) or '{} | {}'.format('','')
        return model_questions

class Answer(models.Model):

    id = models.AutoField(primary_key=True,editable=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        model_answers = str(self.answer) or ''
        return model_answers


class Progress(models.Model):

    class Meta:
        verbose_name_plural = "Progress"
    id = models.AutoField(primary_key=True,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    marks = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        model_progress = '{} | {}'.format(str(self.user),str(self.category)) or '{} | {}'.format('','')
        return model_progress

class Result(models.Model):

    class Meta:
        verbose_name_plural = 'Results'
    id = models.AutoField(primary_key=True,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    correctness = models.BooleanField(default=False)
    

    def __str__(self):
        model_result = '{} | {}'.format(str(self.user),str(self.question)) or '{} | {}'.format('','')
        return model_result


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

@receiver(post_save, sender = User)
def create_auth_token(sender,instance = None, created= False,**kwargs):
    if created:
        Token.objects.create(user=instance)