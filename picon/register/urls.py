from django.urls import path

from . import views



urlpatterns = [
    path('register/', views.AccountList.as_view()),
    path('register/<int:pk>/', views.AccountDetail.as_view()),
    path('home/follow/', views.FollowLog.as_view()),
    path('home/<int:pk>/follow/', views.FollowList.as_view()),
]