
from quiz.models import Question,User,Answer,Result,Progress,Category
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.decorators import api_view



class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'})
    class Meta:
        model = User
        fields = ['username','password','password2']
        extra_kwargs = {
            'password' : {'write_only':True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})

        user = User(username = self.validated_data['username'])
        user.set_password(password)
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class Answerserializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class Progressserializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'
        
class Ressultserializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

#     class Meta: user answer question progress result
#testing api intially
class Categoryserializer(serializers.ModelSerializer):
    class Meta:
         model = Category
         fields = ('id','title',)




# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['id','question','category']


# class Answerserializer(serializers.ModelSerializer):
#     class Meta: