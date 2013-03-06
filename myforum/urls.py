from django.conf.urls import patterns, include, url


urlpatterns = patterns('myforum.views',
    url(r'^$', 'index', name='index'),
    url(r'^topic/(?P<slug>[\w-]+)/$', 'topic_detail', name='topic'),
    
)
