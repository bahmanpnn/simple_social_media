from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register-page'),
    path('login/',views.LoginView.as_view(),name='login-page'),
    path('logout/',views.LogoutView.as_view(),name='logout-page'),
    # path('dispatch',views.TestDispatch.as_view(),name='dispatch'),
    path('profile/<int:user_id>/',views.UserProfileView.as_view(),name='profile-page'),
    #reset password
    path('reset_password/',views.UserPasswordResetView.as_view(),name='reset-password'),
    path('reset_password/done/',views.UserPasswordResetDone.as_view(),name='reset-password-done'),
    path('reset_password/confirm/<uidb64>/<token>/',views.UserPasswordConfirmView.as_view(),name='reset-password-confirm'),
    path('reset_password/complete',views.UserPasswordCompleteView.as_view(),name='reset-password-complete'),


]
