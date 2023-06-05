# from .common import TrackSerializer
from .common import TrackSerializer
from jwt_auth.serializers.common import UserSerializer # this uses absolute path. Absolute paths in django have the manage.py as the root
from artists.serializers.common import ArtistSerializer

class PopulatedTrackSerializer(TrackSerializer):
  # users = UserSerializer(many=True)
  artist = ArtistSerializer(many=True)
