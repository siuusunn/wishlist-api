from django.db import models

# Create your models here.

class Track(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey('artists.Artist', related_name='tracks', on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    isrc = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.artist} - {self.title}"