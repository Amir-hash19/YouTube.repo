from django.db import models
from channle.models import Channel





class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name




class Video(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    channel = models.ForeignKey(to=Channel, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="content/videos/")
    date_uploaded = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(max_length=100)

    VIDEO_STATUS = (
        ("draft", "DRAFT"),
        ("published","PUBLISHED")
    )
    video_status = models.CharField(max_length=20, choices=VIDEO_STATUS, default="draft")

   
  
    tags = models.ManyToManyField(to=Tag, blank=True,related_name="videos_tag")
    slug = models.SlugField(unique=True, max_length=255)


    def __str__(self):
        return f"{self.title}"







class PlayList(models.Model):
    channel = models.ForeignKey(to=Channel, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    video = models.ManyToManyField(to=Video, related_name="videos_Playlist")
    description = models.TextField(null=True, blank=True)

    PLAYLIST_STATUS = (
        ("draft", "DRAFT"),
        ("published","PUBLISHED")
    )

    playlist_status = models.CharField(max_length=20, choices=PLAYLIST_STATUS)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.title}"


