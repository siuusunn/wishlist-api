from django.urls import path
from .views import TrackListView, TrackDetailView, TrackSearchView

urlpatterns = [
    path('', TrackListView.as_view()),
    path('<int:pk>/', TrackDetailView.as_view()),
    path('search/', TrackSearchView.as_view())
]