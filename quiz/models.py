from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import uuid 

class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    id = models.AutoField(primary_key=True,editable=False)
    title = models.CharField(max_length=200)
    def __str__(self):
        s = str(self.title)
        return s 
class Question(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    question = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        # s = {str(self.question),str(self.category)}
        # s = self.question or ''
        s = '{} | {}'.format(str(self.category),str(self.question)) or '{} | {}'.format('','')
        return s 

class Answer(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    def __str__(self):
        s = str(self.answer) or ''
        return s

class Progress(models.Model):
    class Meta:
        verbose_name_plural = "Progress"
    id = models.AutoField(primary_key=True,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    marks = models.IntegerField()
    total = models.IntegerField()
    def __str__(self):
        s = '{} | {}'.format(str(self.user),str(self.category)) or '{} | {}'.format('','')
        return s 

class Result(models.Model):
    class Meta:
        verbose_name_plural = 'Results'
    id = models.AutoField(primary_key=True,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    correctness = models.BooleanField(default=False)
    correct_answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='correct_answer')
    selected_answer  = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='selected_answer')
    def __str__(self):
        s = '{} | {}'.format(str(self.user),str(self.question)) or '{} | {}'.format('','')
        return s 