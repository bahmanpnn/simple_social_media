from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.contrib import messages



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

class DeletePostView(LoginRequiredMixin,View):

    def get(self,request,post_id):
        target_post=Post.objects.get(id=post_id)
        if request.user.id == target_post.author.id:
            target_post.delete()
            messages.success(request,'your post deleted succuessfully',extra_tags='success')
            return redirect(reverse('home:posts-page'))
        else:
            messages.error(request,'you can not delete this post',extra_tags='danger')
            return redirect(reverse('home:home-page'))
