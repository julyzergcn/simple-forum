from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from myforum.models import Forum, Topic, Post
from myforum.utils import login_view


def index(request):
    '''
    List topics
    '''
    context = {
        'topics': Topic.objects.active(),
    }
    return render(request, 'myforum/index.html', context)

def forum_detail(request, slug):
    '''
    List topics of forum
    '''
    current_forum = get_object_or_404(Forum.objects.active(), slug=slug)
    context = {
        'topics': Topic.objects.active().filter(forum=current_forum),
    }
    return render(request, 'myforum/index.html', context)

def topic_detail(request, slug):
    '''
    List topic posts, or create new post if POST method
    '''
    
    current_topic = get_object_or_404(Topic.objects.active(), slug=slug)
    
    # create new post
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return login_view(request)
        
        post = request.POST.get('post', '').strip()
        if len(post) > 0:
            Post.objects.create(topic=current_topic, content=post, created_by=request.user)
        return redirect('myforum:topic', slug=slug)
    
    context = {
        'current_topic': current_topic,
    }
    return render(request, 'myforum/topic.html', context)

@require_POST
def search(request):
    keywords = request.POST.get('kw', '').split()
    if len(keywords)==0:
        topics_searched = []
    else:
        topics_searched = Topic.objects.active()
        posts_searched = Post.objects.active()
        
        for kw in keywords:
            topics_searched = topics_searched.filter(title__icontains=kw) | topics_searched.filter(description__icontains=kw)
            posts_searched = posts_searched.filter(content__icontains=kw)
        
        topics_searched = list(topics_searched)
        for post in posts_searched:
            if post.topic not in topics_searched:
                topics_searched.append(post.topic)
    
    context = {
        'topics_searched': topics_searched,
    }
    return render(request, 'myforum/topics_searched.html', context)
