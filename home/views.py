from typing import Any
from django.http import HttpRequest
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Post,PostComment
from .forms import CreateUpdatePostForm,CommentCreateForm, ReplyCommentForm,PostSearchForm



# def home(request):
#     return render(request,'home/home.html')


class HomeView(View):
    
    def get(self,request):
        posts=Post.objects.all()
        posts=Post.objects.order_by('?')[:4]
        # posts=Post.objects.order_by('-created_date')[:4]
        # posts=Post.objects.all().order_by('-created_date')[:4]

        
        return render(request,'home/home.html',{
            'posts':posts
        })

    def post(self,request):
        pass

class PostView(View):
    form_class=PostSearchForm
    
    def get(self,request):
        posts=Post.objects.order_by('-created_date')
        # posts=Post.objects.all().order_by('created_date')

        if request.GET.get('search'):
            posts=posts.filter(body__contains=request.GET['search'])

        return render(request,'home/posts.html',{
            'posts':posts,'search_form':self.form_class
        })

    def post(self,request):
        pass


class PostDetailView(View):
    form_class=CommentCreateForm
    form_class_reply=ReplyCommentForm

    def setup(self, request, *args, **kwargs):
        self.target_post_instance=get_object_or_404(Post,pk=kwargs['post_id'],slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self,request,*args, **kwargs):
        comments=self.target_post_instance.post_comments.filter(is_reply=False)
        # comments=PostComment.objects.filter(post=target_post,is_reply=False)
        return render(request,'home/post_detail_page.html',{
            'post':self.target_post_instance,
            'comments':comments,
            'comment_form':self.form_class(),
            'reply_form':self.form_class_reply()
        })

    @method_decorator(login_required)
    def post(self,request,*args, **kwargs):
        form=self.form_class(request.POST)

        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=self.target_post_instance
            new_comment.user=request.user
            new_comment.save()
            messages.success(request,'your comment submitted succussfully',extra_tags='success')
        
        return redirect('home:post-detail-page',self.target_post_instance.id,self.target_post_instance.slug)

class DeletePostView(LoginRequiredMixin,View):

    def get(self,request,post_id):
        target_post=get_object_or_404(Post,id=post_id)
        if request.user.id == target_post.author.id:
            target_post.delete()
            messages.success(request,'your post deleted succuessfully',extra_tags='success')
            return redirect(reverse('home:posts-page'))
        else:
            messages.error(request,'you can not delete this post',extra_tags='danger')
            return redirect(reverse('home:home-page'))

class UpdatePostView(LoginRequiredMixin,View):
    form_class=CreateUpdatePostForm
    template_name='home/update_post.html'

    def setup(self, request, *args,**kwargs):
        self.target_post=get_object_or_404(Post,id=kwargs['post_id'])
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

class CreatePostView(LoginRequiredMixin,View):
    form_class=CreateUpdatePostForm
    template_name='home/create_post.html'

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{
            'form':form
        })
    
    def post(self,request):
        form=self.form_class(request.POST)
        
        if form.is_valid():
            cd=form.cleaned_data

            new_post=form.save(commit=False)
            new_post.author=request.user
            new_post.slug=slugify((cd['title'][:20]+"-"+cd['body'][:20]))
            # new_post=Post.objects.create(title=cd['title'],body=cd['body'],author=author)
            new_post.save()

            messages.success(request,'post added successfully',extra_tags='success')
            return redirect(reverse('home:home-page'))
        

class ReplyPostCommentView(LoginRequiredMixin,View):
    form_class=ReplyCommentForm

    def post(self,request,post_id,comment_id):

        target_post=get_object_or_404(Post,id=post_id)
        target_comment=get_object_or_404(PostComment,id=comment_id)

        form=self.form_class(request.POST)
        if form.is_valid():
            new_reply=form.save(commit=False)
            new_reply.user=request.user
            new_reply.post=target_post
            new_reply.reply=target_comment
            new_reply.is_reply=True
            new_reply.save()

            messages.success(request,'your reply submitted succussfully!!',extra_tags='success')
            
        return redirect('home:post-detail-page',target_post.id,target_post.slug)

