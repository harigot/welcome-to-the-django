from django.urls import path
from rest_framework import routers
from .views import BlogPostviewsets



app_name = 'hyper_api'

router = routers.DefaultRouter()
router.register('', BlogPostviewsets, basename='post-list')
urlpatterns = router.urls
