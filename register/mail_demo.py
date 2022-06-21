import sys
from django.utils import timezone
from django.core.mail import send_mail
import random as rnd
from .models import User



port = 465
def password():
    for i in range (1):
        x = rnd.randint(1000,9999)
        return str(x)


def send_pass_by_email(email):
    subject = 'Your account verifiction email'
    massage = password()
    send_mail(subject,massage , 'mahta.moslehi77@gmail.com', [email])
    user_obj = User.objects.get(email = email)
    user_obj.password = massage
    user_obj.last_generated = timezone.now()
    user_obj.save(update_fields=['password','last_generated'])
