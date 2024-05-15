from django.shortcuts import render
from django.views import View
# Create your views here.

# def home(request):
#     return render(request,'home/home.html')


class HomeView(View):
    
    def get(self,request):
        return render(request,'home/home.html')

    def post(self,request):
        pass
