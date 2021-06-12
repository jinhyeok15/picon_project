from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.AccountList.as_view()),  # POST만 가능하게
    path('my/<int:pk>/', views.AccountDetail.as_view()),  # 내 프로필 상세 정보
    path('follow/log/', views.FollowLog.as_view()),  # 지워야할 API
    path('follow/', views.FollowInfo.as_view()),  # 내 follow 추가 or 삭제
    path('follow/<int:pk>/', views.FollowList.as_view()),  # 내 follow 조회
    path('search/', views.UserSearch.as_view()),  # 전체 유저 조회
    path('follow/<int:pk>/search/', views.FollowSearch.as_view()),  # 내 follow 검색 조회
]
