from django.contrib import admin
from myforum.models import Forum, Topic, Post, UserProfile


admin.site.register(Forum)

class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    exclude = ('created_by', )
    verbose_name_plural = 'Posts for this topic'

admin.site.register(Topic,
    inlines = (PostInline, ),
    fields = ('forum', 'title', 'description', 'created_by'),
)

admin.site.register(UserProfile)
