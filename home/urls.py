from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    # path('',views.home,name='home-page'),
    path('',views.HomeView.as_view(),name='home-page'),
    path('posts/',views.PostView.as_view(),name='posts-page'),
    path('posts/<int:post_id>/<slug:post_slug>/',views.PostDetailView.as_view(),name='post-detail-page'),

]
