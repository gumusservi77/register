from django.contrib.auth.backends import ModelBackend

from .models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, password=None, email=None):
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        is_registered = getattr(user, 'is_registered', False)
        return super(EmailBackend, self).user_can_authenticate(user) and is_registered
