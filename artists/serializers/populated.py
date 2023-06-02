from .common import ArtistSerializer
from tracks.serializers.common import TrackSerializer

# genre serializer gets us the standard fields (in this case it's going to return {"id": 1, "name": "Rock"})

class PopulatedArtistSerializer(ArtistSerializer):
  tracks = TrackSerializer(many=True)