# from django.contrib import admin
from django.urls import path,include
from user_auth import views
from .views import update_username, apply_internship


urlpatterns = [
    path("",views.index,name='user_auth'),
    path("int",views.home,name='int'),
    path("register",views.register,name="register"),
    path("login",views.user_login,name="login"),
    path("list",views.list,name="list"), 
    path("profile",views.profile_view,name="profile"),
    path("logout",views.Ulogout,name="logout"),
    path("pro",views.pro,name="pro"),
    path("home",views.home1,name="home"),
    path("update-username/", update_username, name="update_username"),
    path("apply/", apply_internship, name="apply_internship"),
    path('quit_application/<int:application_id>/', views.quit_application, name='quit_application'),
]
