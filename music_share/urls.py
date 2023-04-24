from django.urls import path
from . import views
from .views import SongListView, SongDetailView, play_song, download_song

urlpatterns = [
    path("", views.SongListView.as_view(), name="music_share-home"),
    path("my_songs/", views.my_songs, name="music_share-private_songs"),
    path("upload/", views.upload, name='music_share-upload'),
    path('song/<int:pk>/', views.SongDetailView.as_view(), name='music_share-song-detail'),
    path('play/<int:song_id>/', views.play_song, name='music_share-play-song'),
    path('download/<int:song_id>/', views.download_song, name='music_share-download-song'),
]