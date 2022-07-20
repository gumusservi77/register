from ast import Param
from audioop import reverse
from email import message
from gc import callbacks
from genericpath import exists
from http import client
from os import access
from turtle import update
from urllib  import response 


from register.models import User
from . import serializers
from .mail_demo import password, send_pass_by_email
from project import settings


from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


from django.shortcuts import get_object_or_404 , render
from django.shortcuts import redirect
from django.contrib import messages


class EmailView(APIView):
    queryset = User.objects.all()
    serializer_class = serializers.EmailSerializer

    def post(self , request,*args, **kwargs):

        serializer = serializers.EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_pass_by_email(serializer.data['email'])
            return Response(serializer.data,status=status.HTTP_201_CREATED )

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )



class CodeView(APIView):
    serializer_class = serializers.CodeSerializer


    def post(self, request,*args, **kwargs):  
        serializer = serializers.CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if not user.is_verified:
            user.is_verified = True
            user.is_active = True
            user.save(update_fields = ['is_verified', 'is_active']) 
            id = user.id
            return redirect('http://127.0.0.1:8000/api/confirm/%s/'% id)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmView(APIView):
    serializer_class = serializers.ConfirmSerializer

    def queryset(self):
        user = User.objects.all()
        return user

    def object(self, id):
        return get_object_or_404(self.queryset(), id=id)

    def get(self, request , pk=None):
        id = pk
        if id :
            serializer = serializers.ConfirmSerializer(self.object(id))
        else:
            serializer = serializers.ConfirmSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request,pk=None,*args, **kwargs):
        user = self.object(pk)
        serializer = serializers.ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.is_registered = True
        user.save(update_fields = ['password','is_registered'])
        return Response(status=status.HTTP_204_NO_CONTENT)




class LoginView(APIView):
    serializer_class = serializers.LoginSerializer

    def post(self , request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ChangeView(APIView):
    serializer_class = serializers.ChangeSerializer

    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = User.objects.filter(email = email)
            if not user.exists():
                return Response({'This user is not exists'},status=status.HTTP_400_BAD_REQUEST)
            user=user.first()
            id = user.id
            return redirect('http://127.0.0.1:8000/api/reset/%s/'% id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetView(APIView):
    serializer_class = serializers.ResetSerializer
    model = User

    def get_queryset(self):
        user = User.objects.all()
        return user

    def get_object(self,id):
        return get_object_or_404(self.get_queryset(),id=id)

    def get(self,request,pk=None):
        id = pk
        if id:
            serializer = serializers.ResetSerializer(self.get_object(id))
        else :
            serializer = serializers.ResetSerializer(self.get_queryset(),many=True)
        return Response(serializer.data)

    def post (self, request,pk=None,*args, **kwargs):
        user = self.get_object(pk)
        serializer = serializers.ResetSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.validated_data['password']
            if user.username != username :
                return Response('wrong username' , status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save(update_fields=['password'])

            return Response({'update ': 'password changed'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    serializer_class = serializers.LogoutSerializer

    def post(self, request , *args):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('logout succesfully',status=status.HTTP_204_NO_CONTENT)




class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/accounts/google/login/callback/'
    client_class = OAuth2Client
    # def google_login(request):
    #     redirect_uri = '%s://%s%s'%(
    #         request.schema, request.get_host(),reverse('pain:google_login')
    #     )   
    #     if ('code' in request.GET):
    #         params = {
    #             'grant_type':'authorization_code',
    #             'code':request.GET.get('code'),
    #             'rediret_uri':redirect_uri,
    #             'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
    #             'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
    #         }
    #         url = 'https://accounts.google.com/o/oauth2/token'
    #         response = request.post(url, data=params)
    #         url = 'hhtps://googleapis.com/aouth2/v1/userinfo'
    #         access_token = response.json().get('access_token')
    #         response = request.get(url, Params = {'access_token':access_token})
    #         user_data = request.json()
    #         email = user_data.get('eamil')
    #         if email :
    #             user , _  = User.objects.get_or_create(email= email, username=email)
    #             data = {
    #                 'firdt_name': user_data.get('name', '').split()[0],
    #                 'google_avatar': user_data.get('picture'),
    #                 'is_active' : True
    #             }
    #             user.__dict__.update(data)
    #             user.save()
    #             user.backend = settings.AUTHENTICATION_BACKENDS[0]
    #             # login(request , user)
    #         else :
    #             messages.error(
    #                 request,
    #                 'unable to log in with gmail '
    #             )
    #         id = user.id
    #         return redirect('http://127.0.0.1:8000/api/email/')
    #     else:
    #         url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
    #         scope = [
    #             "https://www.googleapis.com/auth/userinfo.profile",
    #             "https://www.googleapis.com/auth/userinfo.email"
    #         ]
    #         scope = " ".join(scope)
    #         url = url % (settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, scope, redirect_uri)
    #         return redirect(url)
    # serializer_class = serializers.GoogleLoginSerializer
    # def post(self , request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = ((serializer.validated_data)['auth_token'])
    #     return Response(data, status=status.HTTP_200_OK)