from quiz.models import Question,User,Answer,Result,Progress
from rest_framework import serializers
from django.contrib.auth.models import User

class SignUpSerilizer(serializers.ModelSerializer):
    class Meta:



class UserRegserilizer(serializers.ModelSerializer):
    password2 = serializers.CharField( style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['id','email','usename','password','password2']
        extra kwargs
        {
            'password':{'write_only':True}
        }
        def save(self):
            user = User(
                 username = self.validated_data['username'],
                 email= self.validated_data['email'],
                 )
            password = self.validated_data['password'] 
            password1 = self.validated_data['password2']
            if password != password1:
                raise.serializers.ValidationError({'password':'passwords doesnt match'})
            
            user.set_password(password)
            user.save()
            return user

        

class ProgressSerilizer(serializers.ModelSerializer):
    class Meta:

class Ressultserilizer(serializers.ModelSerializer):
    class Meta:

class Categoryserilizer(serializers.ModelSerializer):
    class Meta:

class QuestionSerilizer(serializers.ModelSerializer):
    class Meta:

class AnswerSerilizer(serializers.ModelSerializer):
    class Meta: