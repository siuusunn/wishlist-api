from .common import WishlistSerializer
from jwt_auth.serializers.common import UserSerializer
# from tracks.serializers.common import TrackSerializer
from tracks.serializers import TrackSerializer

class PopulatedWishlistSerializer(WishlistSerializer):
  owner = UserSerializer()
  tracks = TrackSerializer(many=True)