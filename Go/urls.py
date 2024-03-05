from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name="home"),
    path('logout/', views.log_user_out, name='logout'),
    path('login/', views.log_user_in, name="login"),
    path('join/', views.log_user_up, name="registration"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('profile/<str:username>/settings/', views.settings, name='settings'),
    path('profile/<str:username>/play/<str:game_id>/', views.play, name='play'),
]
