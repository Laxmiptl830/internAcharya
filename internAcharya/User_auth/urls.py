# from django.contrib import admin
from django.urls import path,include
from User_auth import views
from .views import update_username, apply_internship


urlpatterns = [
    path("",views.index,name='user_auth'),
    path("home",views.home,name='home'),
    path("register",views.User_register,name="register"),
    path("login",views.user_login,name="login"),
    path("list",views.internship_list_view,name="list"), 
    path("profile",views.profile_view,name="profile"),
    path("logout",views.user_logout,name="logout"),
    path("pro",views.profile_form,name="pro"),
    path("update-username/", update_username, name="update_username"),
    path("apply/", apply_internship, name="apply_internship"),
    path('quit_application/<int:application_id>/', views.quit_application, name='quit_application'),
]
