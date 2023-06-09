# Generated by Django 4.2 on 2023-04-23 07:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_share', '0002_rename_protectmusicfile_protectedmusicfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicfile',
            name='allowed_emails',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), default=list, size=None),
        ),
        migrations.DeleteModel(
            name='ProtectedMusicFile',
        ),
    ]
