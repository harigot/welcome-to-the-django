from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from .models import Post



class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


def PostVoteUp(request, slug, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to vote')
        return redirect('signin')

    post = Post.objects.get(pk=pk)
    post.up_vote += 1
    post.save()

    return redirect('post_detail', slug=slug, pk=pk)


def PostVoteDown(request, slug, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to vote')
        return redirect('signin')
        
    post = Post.objects.get(pk=pk)
    post.down_vote += 1
    post.save()
    return redirect('post_detail', slug=slug, pk=pk)
