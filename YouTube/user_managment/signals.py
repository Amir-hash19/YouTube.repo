from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from .models import UserAccount
import uuid




@receiver(pre_save, sender=UserAccount)
def generate_slug_useraccount(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.username)
        for _ in range(5):
            unique_suffix = str(uuid.uuid4())[:10]
            slug = f"{base_slug}-{unique_suffix}"
            if not UserAccount.objects.filter(slug=slug).exists():
                instance.slug=slug
                break
            else:
                raise ValueError("Could not generate a unique slug for user.")