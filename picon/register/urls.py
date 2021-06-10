from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.AccountList.as_view()),  # POST만 가능하게
    path('my/<int:pk>/', views.AccountDetail.as_view()),  # 내 프로필 상세 정보
    path('follow/log/', views.FollowLog.as_view()),  # 지워야할 API
    path('follow/', views.FollowInfo.as_view()),  # 내 follow 추가 or 삭제
    path('home/<int:pk>/follow/', views.FollowList.as_view()),
    path('search/', views.UserSearch.as_view()),
    path('home/<int:pk>/follow/search/', views.FollowSearch.as_view()),
]
