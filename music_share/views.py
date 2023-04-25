from django.shortcuts import render, redirect, get_object_or_404
from .models import MusicFile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import MusicFileForm
from django.contrib import messages
import eyed3
from django.http import FileResponse
import os
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.conf import settings

@login_required
def upload(request):
    if request.method == "POST":
        form = MusicFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data
            file = form.cleaned_data.get('file')
            visibility = form.cleaned_data.get('visibility')
            allowed_emails = form.cleaned_data.get('allowed_emails')

            # Create MusicFile object
            music_file = MusicFile(owner=request.user, file=file, visibility=visibility)

            # If file is protected, add allowed emails to MusicFile object
            if visibility == 'protected' or visibility == 'Protected':
                music_file.allowed_emails = allowed_emails

            # add the metadata 
            # file_path = settings.MEDIA_ROOT + file.temp
            file_path = file.temporary_file_path()

            audio = eyed3.load(file_path)
            print(audio.tag.title)
            music_file.title = audio.tag.title if audio.tag.title else "Unknown Title"
            music_file.artist = audio.tag.artist if audio.tag.artist else "Unknown Artist"
            music_file.album = audio.tag.album if audio.tag.album else "Unknown Album"
            # music_file.image = audio.tag.images[0] if audio.tag.images else 'default.jpeg'

            # Save MusicFile object to database
            music_file.save()

            messages.success(request, f'Successfully uploaded {file.name}!')

            return redirect('music_share-upload')
    else:
        form = MusicFileForm()

    return render(request, 'music_share/upload.html', {'form': form})


class SongListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MusicFile
    template_name = 'music_share/song_list.html'
    paginate_by = 6

    def test_func(self) -> bool | None:
        # Check if the user is authenticated 
        return self.request.user.is_authenticated 

    def get_queryset(self):
        # Filter the queryset to only include songs owned by the current user, songs which are public and songs which user have access
        queryset = super().get_queryset()
        return queryset.filter(Q(owner=self.request.user) | Q(visibility='public') | Q(allowed_emails__contains=[self.request.user.email]))
    


class UserSongListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MusicFile
    template_name = 'music_share/song_list.html'
    paginate_by = 6

    def test_func(self) -> bool | None:
        # Check if the user is authenticated and the owner of the songs
        return self.request.user.is_authenticated and MusicFile.objects.filter(owner=self.request.user).exists()

    def get_queryset(self):
        # Filter the queryset to only include songs owned by the current user
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class SongPlayView(DetailView):
    model = MusicFile
    template_name = 'music_share/play_song.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['audio_file_url'] = self.object.file.url
        return context
    
    def get(self, request, song_id):
        song = get_object_or_404(MusicFile, id=song_id)
        file_path = song.file.path
        if os.path.exists(file_path):
            context = {
                'song': song
            }
            return render(request, 'music_share/play_song.html', context)
        raise Http404


# @login_required
# def play_song(request, song_id):
#     song = get_object_or_404(MusicFile, id=song_id)
#     file_path = song.file.path
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="audio/mpeg")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404


@login_required
def download_song(request, song_id):
    song = get_object_or_404(MusicFile, id=song_id)
    file_path = song.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/x-download")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404
