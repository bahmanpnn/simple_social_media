from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm,LoginForm
from home.models import Post

class RegisterView(View):
    
    form_class=RegisterForm
    template_name='accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'you logged in and can not register when logged in ;))',extra_tags='danger')
            return redirect(reverse('home:home-page')) 
        else:
            return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            cd=form.cleaned_data
            
            # user=User.objects.filter(email=cd['email']).exists()
            # if user:
            #     messages.error(request,'this user exists!! please register again ;))',extra_tags='danger')
            #     return redirect(reverse('accounts:register-page')) 
            
            User.objects.create_user(username=cd['username'],email=cd['email'],password=cd['password'])
            messages.success(request,'user added succussfully; please login now :)) ',extra_tags='success')
            
            return redirect(reverse('home:home-page'))           
            

        else:
            return render(request,self.template_name,{'form':form}) 


class LoginView(View):

    template_name='accounts/login.html'
    form_class=LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'you logged in and can not login when logged in; so logout first then login ;))',extra_tags='danger')
            return redirect(reverse('home:home-page')) 
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            cd=form.cleaned_data
            check_user=authenticate(request,username=cd['username'],password=cd['password'])
            if check_user is not None:
                login(request,check_user)
                messages.success(request,'you logged in successfully :)))',extra_tags='success')
                return redirect(reverse('home:home-page'))
            # else:
            #     messages.error(request,'your username does not exists!! try again please',extra_tags='danger')
            #     return redirect(reverse('accounts:login-page'))
            messages.error(request,'your username does not exists!! try again please',extra_tags='danger')
            
                
        return render(request,self.template_name,{'form':form})
    

class LogoutView(LoginRequiredMixin,View):
    # login_url='/accounts/login/'

    def get(self,request):
        logout(request)
        messages.success(request,'you logged out succussfully')
        return redirect(reverse('home:home-page'))
    

# class TestDispatch(View):
#     template_name='accounts/dispatch.html'

#     def dispatch(self, request, *args, **kwargs):
#         if request.method=="GET":
#             kwargs['data']='bahman'
#             return self.one(request, *args, **kwargs)
#         elif request.method=="POST":
#             kwargs['data']='mamad'
#             return self.two(request, *args, **kwargs)
#         else:
#             return super().dispatch(request,*args,**kwargs)
    
#     def one(self,request,*args, **kwargs):
#         return render(request,self.template_name,{'data':kwargs['data']})

#     def two(self,request,*args, **kwargs):
#         return render(request,self.template_name,{'data':kwargs['data']})


class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        try:
            user=get_object_or_404(User,pk=user_id)
            user_posts=Post.objects.filter(author_id=user_id)
            user_posts=get_list_or_404(Post,author_id=user_id)
            # user_posts=Post.objects.filter(author=user)
            return render(request,'accounts/profile.html',{'user':user,'posts':user_posts})

        except User.DoesNotExist:
            return redirect(reverse('home:home-page'))