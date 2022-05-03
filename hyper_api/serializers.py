from rest_framework import serializers
from hyperdrated.models import BlogPost



class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('id', 'author', 'title', 'content', 'created_on', 'updated_on', 'status', 'up_vote', 'down_vote')
