from django.urls import path
from . import views

urlpatterns = [
    path("", views.SongListView.as_view(), name="music_share-home"),
    path("my_songs/", views.UserSongListView.as_view(), name="music_share-private-songs"),
    path("upload/", views.upload, name='music_share-upload'),
    # path('play/<int:song_id>/', views.play_song, name='music_share-play-song'),
    path('play/<int:song_id>', views.SongPlayView.as_view(), name='music_share-play-song'),
    path('download/<int:song_id>/', views.download_song, name='music_share-download-song'),
]