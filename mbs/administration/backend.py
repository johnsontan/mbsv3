from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Accounts

UserModel = get_user_model()

class EmailBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None):
        try:
            user = UserModel.objects.get(email__iexact=email)
            if user is not None and user.check_password(password):
                if user.status == Accounts.ACTIVE:
                    return user
        except UserModel.DoesNotExist:
            return None
        return None
