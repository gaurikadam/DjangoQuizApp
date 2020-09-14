
from quiz.models import Question,User,Answer,Result,Progress,Category
# Create your views here.
from rest_framework import generics
from django.shortcuts import render ,get_object_or_404 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import mixins
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



# #With APIView
# class CategoryAPI(APIView):

#     def get(self,request):
#         categories = Category.objects.all()
#         print(categories)
#         serializer = Categoryserializer(categories,many=True)
#         return Response(serializer.data,status=200)


#     def post(self,request):
#         data=request.data
#         serializer = Categoryserializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=201)
#         return Response(serializer.errors,status=400)

###################user register with token################

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

####################### Generic View and List View


class CategoryAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.order_by('id')
    serializer_class = Categoryserializer

class QuestionAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    def get_queryset(self):
        cat_id = self.request['cat_id']
        user = self.request.user
        question_in_result = Question.objects.filter(user = user,question__category__id = cat_id)
        query = Question.objects.filter(category__id = cat_id).exclude(id__in=[o.question.id for o in question_in_result])
        print(query)
        return query

class AnswerAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Answerserializer
    def get_queryset(self):
        question_id = self.kwargs['question_id']
        query_api=  Answer.objects.filter(question__id = question_id)
        return query_api
    
    def create(self):
        user = self.request.user
        data = self.request.data
        question = get_object_or_404(Question,id = data['question'])
        correct_answer = get_object_or_404(Answer,id = data['correct_answer'])
        selected_answer = get_object_or_404(Answer,id = data['selected_answer'])
        is_correct = False
        if data['is_correct'] == 'true':
            is_correct = True
        else:
            is_correct = False
        result = Result.objects.create(user=user,
                            question=question,
                            is_correct=is_correct)

        serializer = Ressultserializer(result)
        return Response(serializer.data)

class ProgressAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Progressserializer
    
    def get_queryset(self):
        user = self.request.user
        qs = Progress.objects.filter(user = user)
        return qs

    def create(self,request):
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
            serializer= Progressserializer(progress)
            return Response(serializer.data)



class ResultAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Ressultserializer
    def get_queryset(self):
        user = self.request.user
        cat_id = self.request['cat_id']
        query = Result.objects.filter(user=user,question__category__id = cat_id)
        return query
        
