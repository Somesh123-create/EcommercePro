from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', Profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact/', contact, name='contact'),

]
