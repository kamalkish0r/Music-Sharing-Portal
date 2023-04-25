from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from PIL import Image

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
    image = models.ImageField(default='default.jpeg', upload_to='album_art')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC)
    title = models.CharField(max_length=150, default="Unknown")
    artist = models.CharField(max_length=50, default="Unknown")
    album = models.CharField(max_length=50, default="Unknown")
    allowed_emails = ArrayField(models.EmailField(), default=list)

    def __str__(self) -> str:
        return self.title, self.artist, self.album, self.visibility
    

    def save(self, *args, **kwargs):
        kwargs['force_insert'] = False
        super(MusicFile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 300:
            output_size = (400, 300)
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
            img.save(self.image.path)

