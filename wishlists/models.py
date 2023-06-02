from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Wishlist(models.Model):

    tracks = models.ManyToManyField('tracks.Track', related_name="wishlists", blank=True)
    owner = models.ForeignKey("jwt_auth.User", related_name="wishlist", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner}'s Wishlist"
