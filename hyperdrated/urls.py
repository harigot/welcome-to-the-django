from django.urls import path
from . import views



app_name = 'hyperdrated'

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('<slug:slug><int:pk>/', views.BlogPostDetail.as_view() , name='post-detail'),
    path('login/', views.Signin.as_view(), name='signin'),
    path('logout/', views.Signout.as_view(), name='signout'),
    path('register/', views.Signup.as_view(), name='signup'),
    path('userpage/', views.UserPage.as_view(), name='userpage'),
    path('activate/<uidb64>/<token>/', views.UserActivate.as_view(), name='activate'),
]
