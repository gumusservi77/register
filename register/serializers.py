from dataclasses import fields
from distutils.log import error
from pyexpat import model
from django.forms import IntegerField
from django.utils import timezone
from django.contrib.auth import password_validation
from django.core import exceptions
import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken ,TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from register.mail_demo import password

from register.models import User
from django.contrib import auth



class EmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    username = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = (

            'id',
            'email',
            'username',

            )

    def validate(self, attrs):
        email = attrs.get('email','')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email is already in use!')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

  

class CodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    code = serializers.CharField(max_length = 4, write_only=True)



    def validate(self, data):
        self.user = User.objects.get(email=data['email'])
        data = super(CodeSerializer, self).validate(data)
        if data['code'] != self.user.password:
                raise serializers.ValidationError('code not correct!!')
        return data



class ConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only = True , style = {'input_type':'password'})
    password_confirm = serializers.CharField(write_only = True , style = {'input_type':'password'})

    def validate_pass(self, attrs):
        try:
            password_validation.validate_password(password=attrs,user=self.instance)
        except exceptions.ValidationError:
            raise serializers.ValidationError()
        return attrs


    def validate(self, data):
        data = super(ConfirmSerializer, self).validate(data)
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('passwords are not match!!')
        return data



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True , style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['username', 'password']


    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def validate(self ,request):
        username = request.get('username','')
        password = request.get('password','')

        user = auth.authenticate(username=username,password=password)

        if not user:
            raise AuthenticationFailed('user not found!')

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        token = self.get_token(user)
        print (token)
        return {'username' : user.username}

 

class ChangeSerializer(serializers.Serializer):
 
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields=['email']

    def validate(self, attrs):
            email = attrs.get('email','')
            if User.objects.filter(email=email).exists():
                return attrs
            else :
                raise serializers.ValidationError({'email': ('email is not exsists!')})

class ResetSerializer(serializers.Serializer):

    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)

    class Meta:
        model=User
        fields='__all__'

        def save(self):
            username=self.validated_data['username']
            password=self.validated_data['password']
            #filtering out whethere username is existing or not, if your username is existing then if condition will allow your username
            if User.objects.filter(username=username).exists():
                #if your username is existing get the query of your specific username 
                user=User.objects.get(username=username)
                #then set the new password for your username
                user.set_password(password)
                user.save()
                return user
            else:
                raise serializers.ValidationError({'error':'please enter valid crendentials'})


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail ('Token is invalid!!')




