from django.db import models
from django.contrib.auth.models import User


class RelationUser(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followings')
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} follows {self.to_user}'
    


    