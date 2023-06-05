from .common import WishlistSerializer
from jwt_auth.serializers.common import UserSerializer
# from tracks.serializers.common import TrackSerializer
from tracks.serializers.common import TrackSerializer
from tracks.serializers.populated import PopulatedTrackSerializer

class PopulatedWishlistSerializer(WishlistSerializer):
  owner = UserSerializer()
  tracks = PopulatedTrackSerializer(many=True)