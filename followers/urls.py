from django.urls import path
from . import views

app_name = 'followers'

urlpatterns = [
    path('followers/list/<username>/', views.FollowerList.as_view(), name='follower_list'),
    path('following/list/<username>/', views.FollowingList.as_view(), name='following_list'),
    path('follow/<username>/', views.FollowUser.as_view(), name='follow'),
    path('unfollow/<username>/', views.UnfollowUser.as_view(), name='unfollow'),
]
