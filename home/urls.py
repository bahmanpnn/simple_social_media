from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    # path('',views.home,name='home-page'),
    path('',views.HomeView.as_view(),name='home-page'),
    path('posts/',views.PostView.as_view(),name='posts-page'),
    path('posts/<int:post_id>/<slug:post_slug>/',views.PostDetailView.as_view(),name='post-detail-page'),
    path('posts/delete/<int:post_id>/',views.DeletePostView.as_view(),name='post-delete'),
    path('posts/update/<int:post_id>/',views.UpdatePostView.as_view(),name='post-update'),
    path('posts/create/',views.CreatePostView.as_view(),name='post-create'),

]
