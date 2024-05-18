from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('register',views.RegisterView.as_view(),name='register-page'),
    path('login',views.LoginView.as_view(),name='login-page'),
    path('logout',views.LogoutView.as_view(),name='logout-page'),
    # path('dispatch',views.TestDispatch.as_view(),name='dispatch'),

]
