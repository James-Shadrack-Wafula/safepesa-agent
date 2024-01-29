from rest_framework import serializers
from .models import QRCodeScan
from .models import Student, Parent
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class QRCodeScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodeScan
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # You can also create a profile instance here if needed
        Parent.objects.create(user=user)

        return user

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
# class UserSerializer(serializers.ModelSerializer):
#     queryset = get_user_model().objects.all()
#     # serializer_class = UserSerializer
#     permission_classes = (IsAuthenticated,)
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Student
        fields = '__all__'
        
class ParentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = Parent
        fields = '__all__'
from . models import TransactionHistory
class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta():
        model = TransactionHistory
        fields = '__all__'

class ChildSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Student
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(required=True)