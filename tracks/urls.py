from django.urls import path
from .views import TrackListView, TrackDetailView

urlpatterns = [
    path('', TrackListView.as_view()),
    path('<int:pk>/', TrackDetailView.as_view())
]