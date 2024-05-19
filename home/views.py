from django.shortcuts import render
from django.views import View
from .models import Post

# def home(request):
#     return render(request,'home/home.html')


class HomeView(View):
    
    def get(self,request):
        posts=Post.objects.all()
        # posts=Post.objects.all().order_by('created_date')

        
        return render(request,'home/home.html',{
            'posts':posts
        })

    def post(self,request):
        pass
