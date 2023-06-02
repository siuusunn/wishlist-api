from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .models import Wishlist
from tracks.models import Track
from .serializers.common import WishlistSerializer
from wishlists.serializers.populated import PopulatedWishlistSerializer

class WishlistListView(APIView):

  permission_classes = [IsAdminUser]

  def get(self, _request):
    wishlist = Wishlist.objects.all()
    serialized_wishlist = PopulatedWishlistSerializer(wishlist, many=True)
    return Response(serialized_wishlist.data, status=status.HTTP_200_OK)


  def post(self, request):
    request.data['owner'] = request.user.id
    wishlist_to_add = WishlistSerializer(data=request.data)
    try:
      wishlist_to_add.is_valid()
      print(wishlist_to_add.errors)
      wishlist_to_add.save()
      return Response(wishlist_to_add.data, status=status.HTTP_201_CREATED)

    except IntegrityError as e:
      res = {
        "detail": str(e)
      }
      return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except AssertionError as e:
      return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except:
      return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class WishlistDetailView(APIView):

  def get_wishlist(self, pk):
    try:
      return Wishlist.objects.get(pk=pk)
    except Wishlist.DoesNotExist:
      raise NotFound(detail="Can't find that wishlist.")

  def get(self, _request, pk):
    try:
      wishlist = self.get_wishlist(pk=pk)
      serialized_wishlist = PopulatedWishlistSerializer(wishlist)
      return Response(serialized_wishlist.data, status=status.HTTP_200_OK)
    except Wishlist.DoesNotExist:
      raise NotFound(detail="Can't find that wishlist. Error code: 2.")

  def put(self, request, pk):
    wishlist_to_update = self.get_wishlist(pk=pk)
    request.data['owner'] = request.user.id
    updated_wishlist = WishlistSerializer(wishlist_to_update, data=request.data)
    try:
      updated_wishlist.is_valid()
      print(updated_wishlist.errors)
      updated_wishlist.save()
      return Response(updated_wishlist.data, status=status.HTTP_202_ACCEPTED)

    except AssertionError as e:
      return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except:
      res = {"detail": "Unprocessable Entity"}
      return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
  def delete(self, request, pk, track_id):
        wishlist = self.get_wishlist(pk)
        try:
            track = wishlist.tracks.get(pk=track_id)
            track.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Track.DoesNotExist:
            raise NotFound(detail="Can't find that track.")
