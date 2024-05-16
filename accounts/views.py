from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages


class RegisterView(View):
    
    form_class=RegisterForm

    def get(self,request):
        form=self.form_class()
        return render(request,'accounts/register.html',{'form':form})
    
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
            return render(request,'accounts/register.html',{'form':form}) 
