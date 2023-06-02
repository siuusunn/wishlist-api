from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from jwt_auth.serializers.common import UserSerializer
from jwt_auth.serializers.populated import PopulatedUserSerializer
from wishlists.serializers.common import WishlistSerializer

User = get_user_model()

class RegisterView(APIView):
  def post(self, request):
    user_to_create = UserSerializer(data=request.data)
    if user_to_create.is_valid():
      user_to_create.save()
      wishlist_to_create = WishlistSerializer(data={
        # "tracks": 0,
        "owner": user_to_create.data["id"]
      })
      if wishlist_to_create.is_valid():
        wishlist_to_create.save()
      return Response({'message:': "Registration successful!"}, status=status.HTTP_201_CREATED)
    return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):

  def post(self, request):
    # get the data from the request
    email = request.data.get('email')
    password = request.data.get('password')
    try:
      user_to_login = User.objects.get(email=email)
    except User.DoesNotExist:
      raise PermissionDenied(detail="Invalid Credentials")
    if not user_to_login.check_password(password):
      raise PermissionDenied(detail="Invalid Credentials")

    dt = datetime.now() + timedelta(days=7) # how long the token will be valid for

    token = jwt.encode(
      {'sub': user_to_login.id, 'exp': int(dt.strftime('%s'))},
      settings.SECRET_KEY,
      algorithm="HS256"
    )

    return Response({'token': token, 'message': f"Welcome back {user_to_login.username}", "is_superuser": user_to_login.is_superuser})

class UserListView(APIView):
  def get(self, _request):
    users = User.objects.all()
    serialized_users = UserSerializer(users, many=True)
    return Response(serialized_users.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):

  # permission_classes = (IsAuthenticated, )

  def get(self, _request, pk):
    try:
      user = User.objects.get(pk=pk)
      serialized_user = UserSerializer(user)
      return Response(serialized_user.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
      raise NotFound(detail="Can't find that user! Your young cousins must've lost them.")

  def put(self, request, pk):
    user_to_edit = User.objects.get(pk=pk)
    updated_user = UserSerializer(user_to_edit, data=request.data)

    try:
      updated_user.is_valid()
      print(updated_user.errors)
      updated_user.save()
      return Response(updated_user.data, status=status.HTTP_202_ACCEPTED)

    except AssertionError as e:
      return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except:
      res = {"detail": "Unprocessable Entity"}
      return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)