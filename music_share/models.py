from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class MusicFile(models.Model):
    ALLOWED_FILE_TYPES = ('mp3', 'wav', 'flac')
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC)
    title = models.CharField(max_length=150, default="Unknown")
    artist = models.CharField(max_length=50, default="Unknown")
    album = models.CharField(max_length=50, default="Unknown")
    allowed_emails = ArrayField(models.EmailField(), default=list)

    def __str__(self) -> str:
        return self.title, self.artist, self.album, self.visibility

