# Generated by Django 5.2.1 on 2025-07-16 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('channle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('caption', models.TextField(blank=True)),
                ('video', models.FileField(upload_to='content/videos/')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField(max_length=100)),
                ('video_status', models.CharField(choices=[('draft', 'DRAFT'), ('published', 'PUBLISHED')], default='draft', max_length=20)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='channle.channel')),
                ('tags', models.ManyToManyField(blank=True, related_name='videos_tag', to='video.tag')),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('description', models.TextField(blank=True, null=True)),
                ('playlist_status', models.CharField(choices=[('draft', 'DRAFT'), ('published', 'PUBLISHED')], max_length=20)),
                ('slug', models.SlugField(unique=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channle.channel')),
                ('video', models.ManyToManyField(related_name='videos_Playlist', to='video.video')),
            ],
        ),
    ]
