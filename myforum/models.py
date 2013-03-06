from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import (
    TimeStampedModel,           # created, modified
    TitleSlugDescriptionModel,  # title, slug, description
    ActivatorModel,                  # status, activate_date, deactivate_date
)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar', blank=True)
    
    def __unicode__(self):
        return self.user.username

class Forum(TitleSlugDescriptionModel):
    order = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('order', )

class Topic(TimeStampedModel, TitleSlugDescriptionModel, ActivatorModel):
    forum = models.ForeignKey(Forum)
    created_by = models.ForeignKey(User)
    order = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('order', '-created')
    
    @models.permalink
    def get_absolute_url(self):
        return ('myforum:topic', [self.slug])
    
    def posts(self):
        return Post.objects.active().filter(topic=self)

class Post(TimeStampedModel, ActivatorModel):
    topic = models.ForeignKey(Topic)
    content = models.TextField()
    created_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.created_by.username + ' said:'
    
    class Meta:
        ordering = ('created', )
    
    def avatar_url(self):
        try:
            return self.created_by.userprofile.avatar.url
        except:
            return '/static/myforum/thumb_default_31_31.jpg'
