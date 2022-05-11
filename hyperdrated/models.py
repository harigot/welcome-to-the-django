from django.contrib.auth.models import User
from django.db import models



STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

VOTE_STATUS = (
    (0,"nope"),
    (1,"yep")
)

class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    status = models.IntegerField(choices=STATUS, default=1)
    up_vote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Voted(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTE_STATUS, default=0)
