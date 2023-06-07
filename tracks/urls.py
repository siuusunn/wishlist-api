from django.urls import path
from .views import TrackListView, TrackDetailView, TrackISRCView

urlpatterns = [
    path('', TrackListView.as_view()),
    path('<int:pk>/', TrackDetailView.as_view()),
    # path('search/', TrackSearchView.as_view()),
    path('<str:isrc>/', TrackISRCView.as_view()),
]