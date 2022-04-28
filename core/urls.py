from django.urls import path
from . import views



urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug><pk>/vote-up/', views.PostVoteUp, name='post_vote_up'),
    path('<slug:slug><pk>/vote-down/', views.PostVoteDown, name='post_vote_down'),
    path('<slug:slug><pk>/', views.PostDetail.as_view(), name='post_detail'),
]
