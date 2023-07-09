from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.getRoute),
    path('rooms/', views.getRooms),
    path('room/<str:pk>/', views.getRoom),
]