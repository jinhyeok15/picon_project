from django.urls import path

from . import views



urlpatterns = [
    path('register/', views.AccountList.as_view()), # POST만 가능하게
    path('my/<int:pk>/', views.AccountDetail.as_view()),
    path('follow/log/', views.FollowLog.as_view()), # 지워야할 API
    path('follow/', views.FollowInfo.as_view()),
    path('home/<int:pk>/follow/', views.FollowList.as_view()),
]