from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Track(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ManyToManyField('artists.Artist', related_name='tracks')
    duration = models.CharField(max_length=5, default="00:00")
    isrc = models.CharField(max_length=12, unique=True)
    added_by = models.ForeignKey("jwt_auth.User", on_delete=models.CASCADE, related_name='wishlist_tracks')

    def __str__(self):
        return f"{', '.join(str(artist) for artist in self.artist.all())} - {self.title}"