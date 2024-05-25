from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    # author=models.ForeignKey(User,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_posts')
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
    
    # class Meta:
    #     ordering=('-created_date',)


class PostComment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_comments')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comments')
    body=models.TextField(max_length=510)
    reply=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='reply_comments')
    # reply=models.ForeignKey('PostComment',null=True,blank=True,on_delete=models.CASCADE)
    is_reply=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'