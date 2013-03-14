from django.contrib import admin
from myforum.models import Forum, Topic, Post, UserProfile, AWS

class AWSAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    list_editable = ('value', )
    list_display_links = ()
    
    def get_actions(self, request):
        return []
    
    def delete_model(self, request, obj):
        if obj.key not in ('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'):
            obj.delete()

admin.site.register(AWS, AWSAdmin)

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
