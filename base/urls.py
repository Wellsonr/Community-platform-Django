from django.urls import path
from . import views

urlpatterns = [
    path ('login/', views.loginPage, name='login'),
    path ('logout/', views.logoutPage, name='logout'),
    path ('singup/', views.signupPage, name='signup'),
    path ('', views.home, name='home'),
    path ('room/<str:pk>/', views.room, name='room'), # <> is use to pass dynamic value in str:and the value name
    path ('profile/<str:pk>/', views.profilePage, name='profile'),
    path ('room-form/', views.createRoom, name='room_form'),
    path('room-update/<str:pk>', views.updateRoom, name='room_update'),
    path('room-delete/<str:pk>', views.deleteRoom, name='room_delete'),
    path('message-delete/<str:pk>', views.deleteMessage, name='message_delete'),
    path('settings/', views.settings, name='settings'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topic/', views.topicPage, name='topic'),
    path('activity/', views.activityPage, name='activity'),
    ]   