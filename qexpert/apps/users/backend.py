from django.conf import settings
from django.contrib.auth.models import check_password
from users.models import UserProfile

class EmailAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self, email=None, password=None):
        """
        Authentication method
        """
        try:
            user = UserProfile.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = UserProfile.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except UserProfile.DoesNotExist:
            return None