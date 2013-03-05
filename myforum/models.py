from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import (
    TimeStampedModel,           # created, modified
    TitleSlugDescriptionModel,  # title, slug, description
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

class Topic(TimeStampedModel, TitleSlugDescriptionModel):
    forum = models.ForeignKey(Forum)
    created_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title

class Post(TimeStampedModel):
    topic = models.ForeignKey(Topic)
    content = models.TextField()
    created_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.created_by.username + ' said:'
    
    class Meta:
        ordering = ('-created', )
