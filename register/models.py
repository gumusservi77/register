from django.core.exceptions import ValidationError
from django.db import models
from django.forms import IntegerField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser , Group






class Group(Group):
    class Meta:
        proxy = True

class User(AbstractUser):
    email = models.EmailField(unique=True , null=False)
    username =  models.CharField (unique=True, max_length = 20,)
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False, editable=False)
    is_registered = models.BooleanField(default=False, editable=False)
    password = models.CharField(unique=True, max_length=4,default=False)
    last_generated = models.DateTimeField(default=timezone.now)

    # REQUIRED_FIELDS =['email']

    def _str_(self):
        return self.email
    

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = 'user_' + str(self.email)
        if self.is_staff or self.is_superuser:
            self.is_verified = True
            self.is_registered = True
        super(User , self).save(*args,**kwargs)

    def clean(self) :
        if not self.email (email__endswith='gmail.come'):
            raise ValidationError('wrong emailadress. please try again')
