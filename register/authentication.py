from django.contrib.auth.models import User
from django.contrib.auth import authenticate

import os
import random
from rest_framework.exceptions import AuthenticationFailed


class EmailAuthBackend(object):
    def authenticate(self, request , email=None,password=None):
        try :
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user (self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None



def register_social_user(provider, user_id, email, username):
    filtered_user_by_email = User.object.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(
                email=email, password=os.onviroon.get('SOCIAL_SECRET')
            )

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'token': registered_user.tokens()
            }
        else :
            raise AuthenticationFailed(detail=' please continue login '+ filtered_user_by_email[0].auth_provider)
    
    else:
        user = {
            'username': EmailAuthBackend(username),'email':email,
            'password': os.onviron.get('SOCIAL_SECRET')
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email = email , password = os.environ.get('SOCIAL-SECRET')
        )

        return {
            'username': new_user.username,
            'email': new_user.email,
            'token': new_user.tokens()
        }