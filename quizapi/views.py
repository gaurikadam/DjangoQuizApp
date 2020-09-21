
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
from rest_framework.permissions import IsAuthenticated,AllowAny
from quizapi.serializers import SignUpSerializer,QuestionSerializer,Categoryserializer,QuestionSerializer,Answerserializer,Progressserializer,Ressultserializer,UserSerializer
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 


# #With APIView

class registrationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = SignUpSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)  

        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        }

        return Response(res)
# serializer = UserCreateSerializer(data=request.data)
#     if not serializer.is_valid():
#         return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)        
#     user = serializer.save()
#     refresh = RefreshToken.for_user(user)
#     res = {
#         "refresh": str(refresh),
#         "access": str(refresh.access_token),
#     }
#     return response.Response(res, status.HTTP_201_CREATED)
    

class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        categories = Category.objects.filter()
        print(categories)
        serializer = Categoryserializer(categories,many=True)
        return Response(serializer.data,status=200)


class QuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        user = self.request.user
        print(user)
        cat_id = pk
        print(pk)
        question_in_result = Result.objects.filter(user=user,question__category__id = cat_id)
        query = Question.objects.filter(category__id = cat_id).exclude(id__in=[o.question.id for o in question_in_result])
        print(query)
        serializer = QuestionSerializer(query,many=True)
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
        serializer = Ressultserializer(result)
        return Response(serializer.data)


class AnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Answerserializer
    def get(self,request,id):
        query = Answer.objects.filter(question__id = id)
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





# class CategoryAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Category.objects.order_by('id')
#     serializer_class = Categoryserializer
# queestion 

# class AnswerAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = Answerserializer
#     def get_queryset(self):
#         question_id = self.request.GET.get('question_id')
#         query_api=  Answer.objects.filter(question__id = question_id)
#         return query_api

    
#     def create(self):
#         user = self.request.user
#         data = self.request.data
#         question = get_object_or_404(Question,id = data['question'])
#         is_correct = False
#         if data['is_correct'] == 'true':
#             is_correct = True
#         else:
#             is_correct = False
#         result = Result.objects.create(user=user,
#                             question=question,
#                             is_correct=is_correct)

#         serializer = Ressultserializer(result)
#         return Response(serializer.data)



# class ProgressAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = Progressserializer
    
#     def get_queryset(self):
#         user = self.request.user
#         qs = Progress.objects.filter(user = user)
#         return qs

#     def create(self,request):
#         user = self.request.user
#         data = self.request.data
#         category_id = data['category'] 
#         category = get_object_or_404(Category,id=category_id)
#         total_questions = Question.objects.filter(category=category).count()
#         try:
#             progress = Progress.objects.get(user=user,category=category)
#             progress.marks += int(data['marks'])
#             progress.save()
#             serializer= Progressserializer(progress)
#             return Response(serializer.data)
#         except Progress.DoesNotExist:
#             progress = Progress.objects.create(user=user,category=category,marks=data['marks'],total=total_questions)
#             serializer= Progressserializer(progress)
#             return Response(serializer.data)


# class ResultAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = Ressultserializer
#     def get_queryset(self):
#         user = self.request.user
#         pk = self.request['pk']
#         print(pk)
#         query = Result.objects.filter(user=user,question__category__id = pk)
#         print(query)
#         return query