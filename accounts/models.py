from django.db import models
from django.contrib.auth.models import User


class RelationUser(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followings')
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} follows {self.to_user}'
    


class ProfileUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age=models.PositiveSmallIntegerField(default=0)
    phone_number=models.CharField(max_length=11,blank=True,null=True)
    bio=models.TextField(max_length=510,blank=True,null=True)

    def __str__(self):
        return self.user.username