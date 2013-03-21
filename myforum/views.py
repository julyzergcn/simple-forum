from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.contrib.auth.views import login as auth_login_view
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import email_re
from django.contrib.auth.models import User

from myforum.models import Forum, Topic, Post, AWS
from myforum.templatetags.myforum_tags import can_edit, can_delete


def signup(request):
    if request.method == 'POST':
        data = request.POST
        if 'email' in data and email_re.search(data['email']):
            username = data.get('username', '')
            password = data.get('password', '')
            email = data['email']
            User.objects.create_user(username, email, password)
            return redirect('myforum:index')
    
    return render(request, 'myforum/signup.html')

def login(request):
    if request.method == 'POST':
        data = request.POST
        if 'email' in data and email_re.search(data['email']):
            password = data.get('password', '')
            email = data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise Http404('User does not exist')
            user = authenticate(username=user.username, password=password)
            if user:
                auth_login(request, user)
            else:
                raise Http404('Invalid password')
            return redirect('myforum:index')
    
    return render(request, 'myforum/login.html')

def login_with_username(request):
    defaults = {
        'template_name': 'admin/login.html',
        'authentication_form': AuthenticationForm,
    }
    return auth_login_view(request, **defaults)

def logout(request):
    auth_logout(request)
    return redirect(request.GET.get('next') or 'myforum:index')

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
        'current_forum': current_forum,
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
            return redirect(resolve_url('myforum:login')+'?next='+request.get_full_path())
        
        post = request.POST.get('post', '').strip()
        if len(post) > 0:
            is_first_time_post = current_topic.is_first_time_post_by(request.user)
            Post.objects.create(topic=current_topic, content=post, created_by=request.user)
            
            try:
                arn = current_topic.arn.strip()
                email = request.user.email
                if len(arn) > 0 and email_re.search(email):
                    import boto
                    conn = boto.connect_sns(AWS.access_key(), AWS.access_key_secret())
                    if is_first_time_post:
                        conn.subscribe(arn, 'email', email)
                    myname = request.user.get_full_name() or request.user.username
                    myname = myname.encode('utf8')
                    conn.publish(arn, myname+' said: \n\n'+post.encode('utf8'), myname+' reply to '+current_topic.title.encode('utf8'))
            except:
                pass
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

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    topic = post.topic
    if can_delete(request.user, post):
        #~ post.status = Post.INACTIVE_STATUS
        #~ post.save(update_fields=['status'])
        post.delete()
    return redirect(request.GET.get('next') or topic)

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    
    if not can_edit(request.user, post):
        raise Http404('No rights to edit post')
    if request.method == 'POST' and 'content' in request.POST:
        post.content = request.POST['content']
        post.save(update_fields=['content', 'modified'])
        context['saved'] = 'saved'
    
    return render(request, 'myforum/edit_post.html', context)

@login_required
def new_topic(request):
    slug = request.REQUEST.get('f', '')
    current_forum = get_object_or_404(Forum, slug=slug)
    
    if request.method == 'POST':
        data = request.POST
        if 'title' in data and len(data['title'].strip()) > 0:
            title = data['title']
            content = data.get('content', '')
            topic = Topic(title=title, description=content, created_by=request.user, forum=current_forum)
            topic.save()
            return redirect('myforum:topic', slug=topic.slug)
    
    context = {
        'current_forum': current_forum,
    }
    return render(request, 'myforum/new_topic.html', context)
