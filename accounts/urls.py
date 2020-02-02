from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('userlist/', views.UserListView.as_view(), name='user_list'),
    path('profilepic/add/', views.AddProfilePicture.as_view(), name='add_prof_pic'),
    path('profilepic/<int:pk>/update/', views.UpdateProfilePicture.as_view(), name='update_prof_pic'),
]
