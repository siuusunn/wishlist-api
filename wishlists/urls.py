from django.urls import path
from .views import WishlistListView, WishlistDetailView

urlpatterns = [
  path('', WishlistListView.as_view()),
  path('<int:pk>/', WishlistDetailView.as_view())
]