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
            User.objects.create_user(username=cd['username'],email=cd['email'],password=cd['password'])
            messages.success(request,'user added succussfully; please login now :)) ',extra_tags='success')
            
            return redirect(reverse('home:home-page'))           
            
            # check_username=User.objects.get(username=new_user.username)
            # if check_username is None:
            #     new_user.save()

        else:
            return render(request,'accounts/register.html',{'form':form}) 
