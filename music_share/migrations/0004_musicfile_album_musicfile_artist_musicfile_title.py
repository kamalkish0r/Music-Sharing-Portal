# Generated by Django 4.2 on 2023-04-24 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_share', '0003_musicfile_allowed_emails_delete_protectedmusicfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicfile',
            name='album',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='musicfile',
            name='artist',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='musicfile',
            name='title',
            field=models.CharField(default='Unknown', max_length=150),
        ),
    ]
