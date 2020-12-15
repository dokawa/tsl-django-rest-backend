from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

from wall_app import views
from wall_app.views import UserViewSet, WallPostViewSet


user_list = UserViewSet.as_view({
    'get': 'list'
})
wall_post_list = WallPostViewSet.as_view({
    'get': 'list',
})
wall_post_create = WallPostViewSet.as_view({
    'get': 'retrieve',
    'post': 'create'
})

urlpatterns = [
    path('', wall_post_list, name='wall-post-detail'),
    # path('admin/', admin.site.urls),
    path('message/', wall_post_create, name='wall-post-list'),
    path('message/<int:pk>/', wall_post_create, name='wall-post-create'),
    # path('users/', user_list, name='user-list'),
    path('register/', views.UserCreate.as_view()),
    path('register-as-guest/', views.AnonymousUserCreate.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('token/', ObtainAuthToken.as_view()),
]
