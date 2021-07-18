from django.urls import path

from . import views


urlpatterns = [
    path('register', views.AccountList.as_view()),  # POST만 가능하게 / MY1
    path('my/<int:pk>', views.AccountDetail.as_view()),  # 내 프로필 상세 정보 / MY2
    path('follow/log', views.FollowLog.as_view()),  # 지워야할 API
    path('follow', views.FollowInfo.as_view()),  # 내 follow 추가 or 삭제 / FLW1
    path('home/<int:pk>/follow', views.FollowList.as_view()),  # 내 follow 조회 / FLW2
    path('search', views.UserSearch.as_view()),  # ?nick_name= / 전체 유저 조회 / U1
    path('follow/<int:pk>/search', views.FollowSearch.as_view()),  # ?nick_name= / 내 follow 검색 조회 / FLW3
    path('upload', views.UploadFile.as_view(), name='file-upload'),  # 파일 업로드 API / UP1
    path('upload/<int:user_id>', views.UserFile.as_view()),  # 파일 상태 수정/조회 API / UP2
    path('profile/<int:user_id>', views.UserProfile.as_view()),  # 프로필 리스트 조회 API / PRF1
    path('contents/<int:user_id>', views.UserContents.as_view()),  # 유저의 이미지 컨텐츠 조회 API / CNT1
    path('home/contents/<int:user_id>', views.HomeContents.as_view()),  # 홈화면 컨텐츠 조회 API / CNT2
]
