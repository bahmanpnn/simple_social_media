from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


class RegisterView(View):
    
    form_class=RegisterForm
    template_name='accounts/register.html'
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
    

class LogoutView(View):
    
    def get(self,request):
        logout(request)
        messages.success(request,'you logged out succussfully')
        return redirect(reverse('home:home-page'))