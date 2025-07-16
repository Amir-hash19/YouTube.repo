from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from user_managment.models import UserAccount


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("reply", "Reply to Comment"),
        ("new_video", "New Video Uploaded"),
        ("like", "Video Liked"),
        ("comment", "New Comment"),
    ]

    recipient = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE, related_name="notifications")  # کسی که اعلان براش هست
    actor = models.ForeignKey(to=UserAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name="actor_notifications")  # کسی که این کار رو کرده
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    target_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')  # مثلاً کامنت، ویدیو، کانال و غیره

    message = models.TextField(blank=True, null=True)  # متن اختیاری برای UI
    url = models.URLField(blank=True, null=True)  # لینک به هدف اعلان
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} -> {self.recipient}"

