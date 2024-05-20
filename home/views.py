from typing import Any
from django.http import HttpRequest
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from .models import Post
from .forms import UpdatePostForm



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

class UpdatePostView(LoginRequiredMixin,View):
    form_class=UpdatePostForm
    template_name='home/update_post.html'

    def setup(self, request, *args,**kwargs):
        self.target_post=Post.objects.get(id=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    

    def dispatch(self, request, *args, **kwargs):
        # target_post=self.target_post
        if not request.user.id == self.target_post.author.id:
            messages.error(request,'you can not update this post!!',extra_tags='danger')
            return redirect('home:home-page')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request,*args, **kwargs):
        # target_post=self.target_post
        return render(request,self.template_name,{
            'form':self.form_class(instance=self.target_post)
        })

    def post(self,request,*args, **kwargs):
        # target_post=self.target_post
        form=self.form_class(request.POST,instance=self.target_post)

        if form.is_valid():
            updated_post=form.save(commit=False)
            updated_post.slug=slugify(form.cleaned_data['title'][:20]+form.cleaned_data['body'][:20])
            updated_post.save()
            
            messages.success(request,'post updated successfully',extra_tags='success')
            return redirect('home:post-detail-page',self.target_post.id,self.target_post.slug)
