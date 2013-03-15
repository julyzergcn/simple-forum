from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_extensions.db.models import (
    TimeStampedModel,           # created, modified
    TitleSlugDescriptionModel,  # title, slug, description
    ActivatorModel,                  # status, activate_date, deactivate_date
)


class AWS(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return self.key
    
    class Meta:
        verbose_name_plural = 'AWS'
    
    @classmethod
    def access_key(cls):
        return cls.objects.get(key='AWS_ACCESS_KEY_ID').value or getattr(settings, 'AWS_ACCESS_KEY_ID', '')
    
    @classmethod
    def access_key_secret(cls):
        return cls.objects.get(key='AWS_SECRET_ACCESS_KEY').value or getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar', blank=True)
    
    def __unicode__(self):
        return self.user.username

class Forum(TitleSlugDescriptionModel, ActivatorModel):
    order = models.IntegerField(default=9)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('order', )
    
    @models.permalink
    def get_absolute_url(self):
        return ('myforum:forum', [self.slug])
    
    def topics_count(self):
        return models.get_model('myforum', 'topic').objects.active().filter(forum=self).count()

class Topic(TimeStampedModel, TitleSlugDescriptionModel, ActivatorModel):
    forum = models.ForeignKey(Forum, null=True, blank=True)
    created_by = models.ForeignKey(User)
    order = models.IntegerField(default=9)
    arn = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('order', '-created')
    
    @models.permalink
    def get_absolute_url(self):
        return ('myforum:topic', [self.slug])
    
    def posts(self):
        return Post.objects.active().filter(topic=self)
    
    def is_first_time_post_by(self, user):
        '''return if user first time post for the topic'''
        return user.pk not in self.post_set.all().values_list('created_by', flat=True)
    
    def save(self, **kwargs):
        super(Topic, self).save(**kwargs)
        
        try:
            import boto
            conn = boto.connect_sns(AWS.access_key(), AWS.access_key_secret())
            res = conn.create_topic(self.slug.encode('utf8'))
            arn = res['CreateTopicResponse']['CreateTopicResult']['TopicArn']
            self.arn = arn
            super(Topic, self).save(update_fields=['arn'])
        except:
            pass

class Post(TimeStampedModel, ActivatorModel):
    topic = models.ForeignKey(Topic)
    content = models.TextField()
    created_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.created_by.username + ' said:'
    
    class Meta:
        ordering = ('-created', )
    
    def avatar_url(self):
        try:
            return self.created_by.userprofile.avatar.url
        except:
            return '/static/myforum/thumb_default_31_31.jpg'
