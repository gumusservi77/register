from genericpath import exists
from turtle import update
from urllib import response
from register.models import User
from . import serializers
from .mail_demo import password, send_pass_by_email


from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect



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