from rest_framework import viewsets
from hyperdrated.models import BlogPost
from .serializers import BlogPostSerializer



class BlogPostviewsets(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pass
