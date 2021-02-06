from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

class Character(models.Model):
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(unique=True, blank=True)
    likes           = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    def save(self, *args, **kwargs):
        self.slug = 'Character'+str(self.id)
        super(Character, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("posts:like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("posts:like-api-toggle", kwargs={"slug": self.slug})
    def __str__(self):
        return self.title
