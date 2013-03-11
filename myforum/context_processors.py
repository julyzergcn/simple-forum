from myforum.models import Forum


def forums(request):
    return {
        'forums': Forum.objects.active(),
    }
