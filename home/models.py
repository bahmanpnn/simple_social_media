from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    slug=models.SlugField(unique=True,db_index=True,null=True)
    title=models.CharField(max_length=127)
    body=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title} - {self.author}'
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", args={"pk": self.pk})
    
    