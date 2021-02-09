from django.contrib import admin
from django.urls import path, include
from .views import (SignUpView, UserLoginView, UserLogoutView, CustomPasswordResetView,UserProfileView, 
DeleteProfileImage, Home, ChatGroupFormView, ChatGroupListView, ChatGroupMessageView)
app_name = 'users'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('group-add/',ChatGroupFormView.as_view(),name="chat-group-add"),
    path('group-list/', ChatGroupListView.as_view(), name='group-list'),
    path('chat/<int:pk>/',ChatGroupMessageView.as_view(),name="chat-group-update"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('delete-image/', DeleteProfileImage.as_view(), name='delete-image'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('', include('django.contrib.auth.urls')),
]
