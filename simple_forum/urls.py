from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('myforum.urls', namespace='myforum')),
    
)

from django.conf import settings as s

urlpatterns += patterns('django.views.static',
    (r'^/static/(?P<path>.*)$', 'serve', {'document_root': s.STATIC_ROOT}),
    (r'^/media/(?P<path>.*)$', 'serve', {'document_root': s.MEDIA_ROOT}),
)
