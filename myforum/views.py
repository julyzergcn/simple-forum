from django.shortcuts import render, get_object_or_404
from myforum.models import Forum, Topic, Post


def index(request):
    context = {
        'topics': Topic.objects.active(),
    }
    return render(request, 'myforum/index.html', context)

def topic_detail(request, slug):
    topic = get_object_or_404(Topic.objects.active(), slug=slug)
    context = {
        'topic': topic,
    }
    return render(request, 'myforum/topic.html', context)
