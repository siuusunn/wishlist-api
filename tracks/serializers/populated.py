from .common import TrackSerializer
from jwt_auth.serializers.common import UserSerializer # this uses absolute path. Absolute paths in django have the manage.py as the root

# genre serializer gets us the standard fields (in this case it's going to return {"id": 1, "name": "Rock"})

class PopulatedItemSerializer(TrackSerializer):
  users = UserSerializer(many=True)


# the populated genre serializer will get all the usual keys from the genre serializer
# but will add another which is populated by the Album Serializer