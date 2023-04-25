# MusicShare

MusicShare is a web application developed using Django that allows users to upload, listen and manage their music files. While uploading user can choose to keep file as public, private or protected. Protected files will be visible to allowed users only.
This README file provides information on how to set up the application, how to run it, and how to use its features.

## Setup

##### Clone The Repository

```bash
git https://github.com/kamalkish0r/Music-Sharing-Portal.git
```

##### Create a virtual environment

On linux/mac

```bash
python3 -m venv env
```

On Windows

```bash
python -m venv env
```

##### Activate the virtual environment

On linux/mac

```bash
source env/bin/activate
```

On Windows

```bash
.\env\Scripts\Activate.ps1
```

##### Install dependencies

```bash
pip3 install -r requirements.txt
```

##### Setup Database

Paste the following into `setting.py` inside `django_project` folder by entering required parameters.

```
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_db_name',
        'HOST': 'localhost',
        'USER': 'your_postgres_username',
        'PASSWORD': 'your_postgres_password',
    }
}
```

##### To run the app

```bash
python3 manage.py runserver
```

The application can be accessed at `http://127.0.0.1:8000/` in a web browser.

## Features

#### MusicLib provides the following features:

- User registration and login
- Uploading music files
- Listening to music
- Download music
  <!-- - Editing music file metadata (artist, title, album) -->
  <!-- - Searching for music files by title, artist or album -->
  <!-- - Deleting music files -->
- Updating user profile information
- Resetting passwords through email
