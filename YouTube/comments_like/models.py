from django.db import models
from video.models import Video
from user_managment.models import UserAccount





class Comment(models.Model):
    video = models.ForeignKey(to=Video, on_delete=models.CASCADE, related_name="video_comments")
    user = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE, related_name="userـcomments")
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

    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, blank=True,  related_name="reaction_comments")
    video = models.ForeignKey(to=Video, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE, related_name="user_reaction")
    value = models.CharField(choices=LIKE_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['comment', 'user'], name="unique_comment_user"),
            models.UniqueConstraint(fields=['video', 'user'], name="unique_video_user")
        ]


    def __str__(self):
        return f"{self.user.username} {self.value}d comment {self.comment.id}"    
