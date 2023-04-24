from django.shortcuts import render, redirect
from .models import MusicFile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import MusicFileForm
from django.contrib import messages
import eyed3
import os
from django.conf import settings

@login_required
def home(request):
    all_songs = MusicFile.objects.filter(Q(owner=request.user) | Q(visibility='public') | Q(allowed_emails__contains=[request.user.email]))
    context = {
        'songs' : all_songs
    }
    return render(request, 'music_share/home.html', context)

@login_required
def my_songs(request):
    context = {
        'songs' : MusicFile.objects.filter(owner = request.user)
    }
    return render(request, 'music_share/home.html', context)


def about(request):
    return render(request, 'music_share/about.html', {'title': 'About'})


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

            # Save MusicFile object to database
            music_file.save()

            messages.success(request, f'Successfully uploaded {file.name}!')

            return redirect('music_share-upload')
    else:
        form = MusicFileForm()

    return render(request, 'music_share/upload.html', {'form': form})



from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.conf import settings
import os
from .models import MusicFile


class SongListView(ListView):
    model = MusicFile
    template_name = 'music_share/song_list.html'
    paginate_by = 10


class SongDetailView(DetailView):
    model = MusicFile
    template_name = 'music_share/song_detail.html'


def play_song(request, song_id):
    song = get_object_or_404(MusicFile, id=song_id)
    file_path = song.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="audio/mpeg")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def download_song(request, song_id):
    song = get_object_or_404(MusicFile, id=song_id)
    file_path = song.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/x-download")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404
