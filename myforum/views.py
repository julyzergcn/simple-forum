from django.shortcuts import render
from myforum.models import Forum, Topic, Post


def index(request):
    context = {
        'forums': Forum.objects.all(),
    }
    return render(request, 'myforum/index.html', context)

