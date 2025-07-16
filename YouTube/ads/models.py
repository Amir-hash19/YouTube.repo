from django.db import models
from user_managment.models import UserAccount





class Advertiser(models.Model):
    user = models.OneToOneField(to=UserAccount, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    contact_email = models.EmailField(unique=True)
    approved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.business_name
    



class AdVideo(models.Model):
    advertiser = models.ForeignKey(to=Advertiser, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="ads/videos/")
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    ADS_VIDEO = (
        ("deactive", "DEACTIVE"),
        ("active", "ACTIVE")
    )
    advideo_status = models.CharField(max_length=20, choices=ADS_VIDEO, default="deactive")

    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.title} - {self.advertiser.business_name}"
    


