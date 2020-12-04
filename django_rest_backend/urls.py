"""django_rest_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

from wall_app import views
from wall_app.views import UserViewSet, WallPostViewSet

from rest_framework.authtoken.views import obtain_auth_token

user_list = UserViewSet.as_view({
    'get': 'list'
})
wall_post_list = WallPostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
wall_post_create = WallPostViewSet.as_view({
    'get': 'retrieve',
    'post': 'create'
})

urlpatterns = [
    path('', wall_post_list, name='wall-post-detail'),
    # path('admin/', admin.site.urls),
    path('message/', wall_post_list, name='wall-post-list'),
    path('message/<int:pk>/', wall_post_create, name='wall-post-create'),
    path('users/', user_list, name='user-list'),
    path('register/', views.UserCreate.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('token/', ObtainAuthToken.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
]
