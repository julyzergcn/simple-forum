from django.shortcuts import render, get_object_or_404, redirect
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
