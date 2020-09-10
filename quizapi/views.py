
from quiz.models import Question,User,Answer,Result,Progress
# Create your views here.
from django.shortcuts import render ,get_object_or_404 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quizapi.serializers import SignUpSerilizer
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework import status


@api_view(['POST',])

def registration_view(request):
    if request. method == 'POST':
        serializer = SignUpSerilizer(data=request.data)
        data = {}
        if serializer.is_valid():

            user = serializer.save()
            data['response'] = 'updated user details'
            data['email'] = user.email
            data['username'] = user.username
            
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        print(data)
        return Response(data)

# @api_view(['GET'])
# def question_view(request):
#     try:
#         question = Question.objects.all()
#     except Question.DoesNotExist:
#         return HttpResponse(status=404)
#     if request.method == 'GET':
#         serializer = QuestionSerializer(question)
#         return JsonResponse(serializer.data)
