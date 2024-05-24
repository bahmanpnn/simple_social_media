from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.urls import reverse,reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views 
from .forms import RegisterForm,LoginForm
from .models import RelationUser
# from home.models import Post


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
            posts=user.user_posts.order_by('-created_date') #user_posts is related_name of author in post model
            # user_posts=Post.objects.filter(author_id=user_id)
            # user_posts=Post.objects.filter(author=user)
            # user_posts=get_list_or_404(Post,author_id=user_id)

            is_following=False
            relation=RelationUser.objects.filter(from_user=request.user,to_user=user_id)
            if relation.exists():
                is_following=True

            return render(request,'accounts/profile.html',{'user':user,'posts':posts,'is_following':is_following})

        except User.DoesNotExist:
            return redirect(reverse('home:home-page'))
        

#reset password views

class UserPasswordResetView(auth_views.PasswordResetView):
    template_name='accounts/email/reset_password.html'
    success_url=reverse_lazy('accounts:reset-password-done') #reverse_lazy when all templates load acts(when class done)
    email_template_name='accounts/email/reset_password_email.html'


class UserPasswordResetDone(auth_views.PasswordResetDoneView):
    template_name='accounts/email/reset_password_done.html'

class UserPasswordConfirmView(auth_views.PasswordResetConfirmView):
    '''
        this class works on email link that user recieve and click on it then this class and url load,
        so this url has form that load for changing user password
    '''
    template_name='accounts/email/reset_password_confirm.html'
    success_url=reverse_lazy('accounts:reset-password-complete')

class UserPasswordCompleteView(auth_views.PasswordResetCompleteView):
    template_name='accounts/email/reset_password_complete.html'


#follow and unfollow views

class UserFollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(id=user_id)
        if not RelationUser.objects.filter(from_user=request.user,to_user=user).exists():
            new_follow=RelationUser.objects.create(from_user=request.user,to_user=user)
            new_follow.save()
            messages.success(request,'you followed this user')
        else:
            messages.error(request,'you followed this user before',extra_tags='danger')
        return redirect('accounts:profile-page',user_id)



class UserUnFollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(id=user_id)
        relation=RelationUser.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request,'you unfollowed this user',extra_tags='success')
        else:
            messages.error(request,'you are not following this user and can not unfollow!!',extra_tags='danger')
        
        return redirect('accounts:profile-page',user.id)
    
    
# class UserFollowView(LoginRequiredMixin,View):
#     def get(self,request,user_id):
#         if not RelationUser.objects.filter(from_user=request.user,to_user=user_id).exists():
#             new_follow=RelationUser.objects.create(from_user=request.user,to_user=user_id)
#             new_follow.save()
#             messages.success(request,'you followed this user')
#         else:
#             messages.error(request,'you followed this user before',extra_tags='danger')
#         return redirect('accounts:profile-page',user_id)


# class UserUnFollowView(LoginRequiredMixin,View):
#     def get(self,request,user_id):
#         relation=RelationUser.objects.filter(from_user=request.user,to_user=user_id)
#         if relation.exists():
#             relation.delete()
#             messages.success(request,'you unfollowed this user',extra_tags='success')
#         else:
#             messages.error(request,'you are not following this user and can not unfollow!!',extra_tags='danger')
        
#         return redirect('accounts:profile-page',user_id)