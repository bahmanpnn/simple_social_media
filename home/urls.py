from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    # path('',views.home,name='home-page'),
    path('',views.HomeView.as_view(),name='home-page'),

]
