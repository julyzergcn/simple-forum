from django.contrib import admin
from myforum.models import Forum, Topic, Post, UserProfile


admin.site.register(Forum,
    list_display = ('title', 'status', 'order'),
    list_editable = ('order', ),
    fields = ('title', 'description', 'status'),
)

class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('content', 'status', 'created_by')
    verbose_name_plural = 'Posts for this topic'

class TopicAdmin(admin.ModelAdmin):
    inlines = (PostInline, )
    fields = ('forum', 'title', 'description', 'status')
    list_display = ('title', 'status', 'created_by', 'order')
    list_editable = ('order', )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

admin.site.register(Topic, TopicAdmin)

admin.site.register(UserProfile)
