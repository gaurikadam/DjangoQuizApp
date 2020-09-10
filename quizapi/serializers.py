from quiz.models import Question,User,Answer,Result,Progress
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.decorators import api_view



class SignUpSerilizer(serializers.ModelSerializer):
    password2 = serializers.CharField( style={'input_type':'password'})
    class Meta:
        model = User
        fields = ['email','username','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

        def save(self):
            user = User(
                email= self.validated_data['email'],
                 username = self.validated_data['username'],
                 
                 )
            password = self.validated_data['password'] 
            password1 = self.validated_data['password2']
            if password != password1:
                raise serializers.ValidationError({'password':'Passwords must match'})
            
            user.set_password(password)
            
            return user

        

# class Progressserializer(serializers.ModelSerializer):
#     class Meta:

# class Ressultserializer(serializers.ModelSerializer):
#     class Meta:

# class Categoryserializer(serializers.ModelSerializer):
#     class Meta:

# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['id','question','category']


# class Answerserializer(serializers.ModelSerializer):
#     class Meta: