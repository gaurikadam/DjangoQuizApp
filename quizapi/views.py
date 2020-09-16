
from quiz.models import Question,User,Answer,Result,Progress,Category
# Create your views here.
from rest_framework import generics
from django.shortcuts import render ,get_object_or_404 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import mixins
import logging
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quizapi.serializers import SignUpSerializer,QuestionSerializer,Categoryserializer,QuestionSerializer,Answerserializer,Progressserializer,Ressultserializer,UserSerializer
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework import status
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 


# #With APIView

class registrationAPIView(APIView):
    permission_classes = []
    def post(self,request):
        serializer = SignUpSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully registered the user'
            data['username'] = user.username

            token = Token.objects.get(user = user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        categories = Category.objects.filter(id=pk)
        print(categories)
        serializer = Categoryserializer(categories,many=True)
        return Response(serializer.data,status=200)


class QuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        user = request.user
        question_in_result = Result.objects.filter(user=user,question__category__id = pk)
        query = Question.objects.filter(category__id = pk).exclude(id__in=[o.question.id for o in question_in_result])
        serializer = QuestionSerializer(question_in_result,many=True)
        return Response(serializer.data,status=200)


    def post(self,request,pk):
        user = self.request.user
        data = self.request.data
        print(data)
        question = get_object_or_404(Question,id = data['question'])
        print(question)
        correctness = False
        if data['is_correct'] == 'true':
            correctness = True
        else:
            correctness = False
        result = Result.objects.create(user=user,
                            question=question,
                            is_correct=correctness)
        result.save()
        serializer = QuestionSerializer(result)
        return Response(serializer.data)


class AnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Answerserializer
    def get(self,request,id):
        print(id)
        query = Answer.objects.filter(question__id = id)
        # query_api= Answer.objects.filter(question__id = 1)
        serializer = Answerserializer(query,many=True)
        return Response(serializer.data,status=200)



class ProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Progressserializer
    
    def get(self,request):
        user = self.request.user
        query = Progress.objects.filter(user = user)
        serializer = Progressserializer(query,many=True)
        return Response(serializer.data,status=200)


    def post(self,request):
        user = self.request.user
        data = self.request.data
        category_id = data['category'] 
        category = get_object_or_404(Category,id=category_id)
        total_questions = Question.objects.filter(category=category).count()
        try:
            progress = Progress.objects.get(user=user,category=category)
            progress.marks += int(data['marks'])
            progress.save()
            serializer= Progressserializer(progress)
            return Response(serializer.data)
        except Progress.DoesNotExist:
            progress = Progress.objects.create(user=user,category=category,marks=data['marks'],total=total_questions)
            progress.save()
            serializer= Progressserializer(progress)
            return Response(serializer.data)



class ResultAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        user = request.user
        result = Result.objects.filter(user=user,question__category__id = pk)
        serializer = Ressultserializer(result,many=True)
        return Response(serializer.data,status=200)




