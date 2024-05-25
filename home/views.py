from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from .models import Post,PostComment
from .forms import CreateUpdatePostForm



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
    
    def get(self,request):
        posts=Post.objects.order_by('-created_date')
        # posts=Post.objects.all().order_by('created_date')

        
        return render(request,'home/posts.html',{
            'posts':posts
        })

    def post(self,request):
        pass


class PostDetailView(View):
    
    def get(self,request,post_id,post_slug):
        target_post=get_object_or_404(Post,pk=post_id,slug=post_slug)
        comments=target_post.post_comments.filter(is_reply=False)
        # comments=PostComment.objects.filter(post=target_post,is_reply=False)
        return render(request,'home/post_detail_page.html',{
            'post':target_post,
            'comments':comments
        })

    def post(self,request):
        pass

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
        
