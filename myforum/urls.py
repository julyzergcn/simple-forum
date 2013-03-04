from django.conf.urls import patterns, include, url


urlpatterns = patterns('myforum.views',
    url(r'^$', 'index', name='index'),
    
)
