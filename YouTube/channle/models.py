from django.db import models
from user_managment.models import UserAccount
from ads.models import AdVideo



class Channel(models.Model):
    title = models.CharField(unique=True, max_length=255)
    bio = models.TextField()
    owner = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE, related_name="owner_channels")
    admins = models.ManyToManyField(to=UserAccount, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="channels/pictures/", null=True, blank=True)
    subscribers = models.ManyToManyField(to=UserAccount, related_name="subscribed_channels", blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.title}"
    




class SocialPlatform(models.TextChoices):
    WEBSITE = 'website', 'Website'
    INSTAGRAM = 'instagram', 'Instagram'
    FACEBOOK = 'facebook', 'Facebook'
    TWITTER = 'twitter', 'Twitter'
    GITHUB = "github", "GitHub"
    OTHER = 'other', 'Other'




class SocialLink(models.Model):
    channel = models.ForeignKey(to=Channel, on_delete=models.CASCADE, related_name="social_channel")
    adsvideo_link = models.ForeignKey(to=AdVideo, on_delete=models.CASCADE, related_name="advideo_links")
    platform = models.CharField(max_length=50, choices=SocialPlatform.choices)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)



    def __str__(self):
        return f"{self.platform}"

