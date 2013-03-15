from django.conf.urls import patterns, include, url


urlpatterns = patterns('myforum.views',
    url(r'^signup/', 'signup', name='signup'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    
    url(r'^$', 'index', name='index'),
    url(r'^forum/(?P<slug>[\w-]+)/$', 'forum_detail', name='forum'),
    url(r'^topic/new/$', 'new_topic', name='new_topic'),
    url(r'^topic/(?P<slug>[\w-]+)/$', 'topic_detail', name='topic'),
    url(r'^search/$', 'search', name='search'),
    url(r'^post/(\d+)/delete/$', 'delete_post', name='delete_post'),
    url(r'^post/(\d+)/edit/$', 'edit_post', name='edit_post'),
    
)
