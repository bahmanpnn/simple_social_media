from django.shortcuts import render
from django.views import View
from .models import Post

# def home(request):
#     return render(request,'home/home.html')


class HomeView(View):
    
    def get(self,request):
        posts=Post.objects.all()
        posts=Post.objects.all().order_by('-created_date')[:4]

        
        return render(request,'home/home.html',{
            'posts':posts
        })

    def post(self,request):
        pass

class PostView(View):
    
    def get(self,request):
        posts=Post.objects.all()
        # posts=Post.objects.all().order_by('created_date')

        
        return render(request,'home/posts.html',{
            'posts':posts
        })

    def post(self,request):
        pass


class PostDetailView(View):
    
    def get(self,request,post_id,post_slug):
        target_post=Post.objects.get(pk=post_id,slug=post_slug)
        return render(request,'home/post_detail_page.html',{
            'post':target_post
        })

    def post(self,request):
        pass

