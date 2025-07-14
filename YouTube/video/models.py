from django.db import models
from channle.models import Channel




class Video(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    channel = models.ForeignKey(to=Channel, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="content/videos/")
    date_uploaded = models.DateTimeField(auto_now_add=True)
    #comments
    #likes/dislikes
    slug = models.SlugField(unique=True)


    def __str__(self):
        return f"{self.title}"


