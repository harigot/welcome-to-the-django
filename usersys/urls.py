from django.urls import path
from . import views



urlpatterns = [
    #path('', views.home, name='home'),
    path('login/', views.signin, name='signin'),
    path('register/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('userpage/', views.publicate, name='userpage'),
]
