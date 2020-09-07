
from quiz.models import Question,User,Answer,Result,Progress
# Create your views here.
from django.shortcuts import render ,get_object_or_404 
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from quizapi.serializers import UserRegserilizer

@APIView(['POST'])
def registration_view(request):
    if request. method == 'POST':
        serializer = UserRegserilizer(data=request.data)
        data = {}
        if serializer.is_valid:
            user = serializer.save()
            data['response'] = 'updated user details'
            data['username'] = user.username
            data['email'] = user.email
        else:
            data = serializer.errors

        return Response(data)