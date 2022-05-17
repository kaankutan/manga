from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

# Create your models here.


class Chapter(models.Model):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    pages = ArrayField(models.CharField(max_length=256))
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Manga(models.Model):
    title = models.CharField(max_length=256)
    language = models.CharField(max_length=2)
    slug = models.CharField(max_length=256)
    description = models.CharField(max_length=8196)
    thumbnail = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_draft = models.BooleanField(default=False)
    categories = ArrayField(models.CharField(max_length=64))
    chapters = models.ManyToManyField(Chapter)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.language}/manga/{self.slug}/'


class Viewer(models.Model):
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip


class Slider(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    thumbnail = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    language = models.CharField(max_length=2)

    def __str__(self):
        return self.title
