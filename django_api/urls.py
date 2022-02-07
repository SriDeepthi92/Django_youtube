"""django_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from core.views import Oauth2CallbackView, HomeView, AuthorizeView
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('users.urls')),
    #path('', include('core.urls', 'core'),
    #path('', user_views.home, name='home'),
    path('authorize/', AuthorizeView.as_view(), name='authorize'),
    #path('register/', user_views.register, name='register'),
    #path('video/', HomePageView.as_view(), name='video'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('oauth2callback/', Oauth2CallbackView.as_view(),name='oauth2callback'),
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('home/', HomeView.as_view() , name='home'),
    path('logout', LogoutView.as_view()),
    path('home/result/', views.result, name='result'),



]
