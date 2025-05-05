from django.contrib.auth.backends import ModelBackend
from membership.models import Users

class MobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        mobile = kwargs['mobile']
        try:
            user = Users.objects.get(mobile=mobile)
        except Users.DoesNotExist:
            pass