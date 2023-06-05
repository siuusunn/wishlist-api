# Extends custom view
from rest_framework.views import APIView
# Provides a way for HTTP responses
from rest_framework.response import Response
# Provides a list of response codes
from rest_framework import status
# Provides a default response for a not found
from rest_framework.exceptions import NotFound
# For ValidationError
from django.db import IntegrityError

from rest_framework import generics
from django.db.models import Q

from .models import Track
from .serializers.common import TrackSerializer
from .serializers.populated import PopulatedTrackSerializer

# Create your views here.

class TrackListView(APIView):

    def get(self, _request):
        tracks = Track.objects.all() # Get everything from the tracks table in the database
        serialized_tracks = PopulatedTrackSerializer(tracks, many=True) # Run them through the serializer
        return Response(serialized_tracks.data, status=status.HTTP_200_OK) # Return a response and a status
    
    def post(self, request):
        track_to_add = TrackSerializer(data=request.data)
        try:
            track_to_add.is_valid()
            track_to_add.save()
            return Response(track_to_add.data, status=status.HTTP_201_CREATED)
        
        # Missing any required field error
        except IntegrityError as e:
            res ={
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # Incorrect type error
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # Fallback for any other errors
        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        

class TrackDetailView(APIView):
    
    def get_track(self, pk):
        try:
            return Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            raise NotFound(detail="Can't find that track!")

    def get(self, _request, pk):
        track = self.get_track(pk=pk)
        serialized_track = PopulatedTrackSerializer(track)
        return Response(serialized_track.data, status=status.HTTP_200_OK)
    
class TrackSearchView(APIView):
    
    def get(self, request):
        isrc = request.query_params.get('isrc', '')
        tracks = Track.objects.filter(isrc__icontains=isrc)
        serialized_tracks = PopulatedTrackSerializer(tracks, many=True)
        try:
          return Response(serialized_tracks.data, status=status.HTTP_200_OK)
        except Track.DoesNotExist:
            raise NotFound(detail="Can't find that track!")
    