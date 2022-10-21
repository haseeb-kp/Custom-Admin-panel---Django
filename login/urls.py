from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.index, name="index"),
    path('user_login', views.user_login, name="user_login"),
    path('signup', views.signup, name="signup"),
    path('home', views.home, name="home"),
    path('user_logout',views.user_logout, name="user_logout"),
    path('admin_login',views.admin_login, name="admin_login"),
    path('admin_dashboard',views.admin_dashboard, name="admin_dashboard"),
    path('admin_logout',views.admin_logout, name="admin_logout"),
    path('edit_user/<int:id>/',views.edit_user, name="edit_user"),
    path('add_user',views.add_user, name="add_user"),
    path('delete_user/<int:id>/',views.delete_user, name="delete_user"),


    ]