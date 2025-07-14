from django.db import models
from video.models import Video
from user_managment.models import UserAccount





class Comment(models.Model):
    video = models.ForeignKey(to=Video, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )


    @property
    def is_reply(self):
        return self.parent is not None
    




class LikeDislike(models.Model):

    LIKE_CHOICES = (
        ("like", "Like"),
        ("dislike", "Dislike")
    )    

    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name="likes_dislikes")
    user = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("comment", "user")


    def __str__(self):
        return f"{self.user.username} {self.value}d comment {self.comment.id}"    
