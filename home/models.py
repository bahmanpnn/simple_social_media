from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=127)
    slug=models.SlugField(unique=True,db_index=True,null=True)
    body=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title} - {self.author}'
    
    # def get_absolute_url(self):
    #     """
    #         i dont know why it does not work :(( !!! 
    #     """
    #     return reverse("home:post-detail-page", args=(self.id,self.slug))
    #     return reverse("home:post-detail-page", args=[str(self.id),self.slug])
    #     return reverse("home:post-detail-page", kwargs={"post_id": str(self.id),"post_slug":self.slug})
    