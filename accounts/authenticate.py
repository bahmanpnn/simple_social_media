from django.contrib.auth.models import User


class EmailBackend:

    def authenticate(self,request,username=None,password=None):
        try:
            user=User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
            
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        '''
            this method runs after user and password are ok and
            user finds, now must send user id to view to use
        '''
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None