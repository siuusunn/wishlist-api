from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db import IntegrityError

from .serializers.common import ArtistSerializer
from .serializers.populated import PopulatedArtistSerializer
from .models import Artist

class ArtistListView(APIView):

  def get(self, _request):
    artists = Artist.objects.all()
    serialized_artists = ArtistSerializer(artists, many=True)
    return Response(serialized_artists.data, status=status.HTTP_200_OK)

  def post(self, request):
    artist_to_add = ArtistSerializer(data=request.data)
    try:
      artist_to_add.is_valid()
      artist_to_add.save()
      return Response(artist_to_add.data, status=status.HTTP_201_CREATED)

    except IntegrityError as e:
      res = {
        "detail": str(e)
      }
      return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except AssertionError as e:
      return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except:
      return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ArtistDetailView(APIView):

  def get_artist(self, pk):
    try:
      return Artist.objects.get(pk=pk)
    except Artist.DoesNotExist:
      raise NotFound(detail="Can't find that artist!")

  def get(self, _request, pk):
      artist = self.get_artist(pk=pk)
      serialized_comment = PopulatedArtistSerializer(artist)
      return Response(serialized_comment.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    artist_to_edit = self.get_artist(pk=pk)
    updated_artist = ArtistSerializer(artist_to_edit, data=request.data)
    try:
      updated_artist.is_valid()
      updated_artist.save()
      return Response(updated_artist.data, status=status.HTTP_202_ACCEPTED)
    
    # Assertion Error is when we pass in incorrect data type
    except AssertionError as e:
      return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Or any other exceptions
    except:
      return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

  def delete(self, _request, pk):
    artist_to_delete = self.get_artist(pk=pk)
    artist_to_delete.delete()
    return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)