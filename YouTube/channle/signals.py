from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete
from django.utils.text import slugify
from .models import Channel
import uuid





receiver(pre_save, sender=Channel)
def generate_slug_for_channel(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        for _ in range(5):
            unique_suffix = str((uuid.uuid4()))[:10]
            slug = f"{base_slug}-{unique_suffix}"
            if not Channel.objects.filter(slug=slug).exists():
                instance.slug = slug
                break
            else:
                raise ValueError("Couldn't generate a unique slug for channel.")
            



receiver(post_save, sender=Channel)
def set_admin_channel_true(sender, instance, created,**kwargs):
    if created:
        owner = instance.owner
        if not owner.is_channel_admin:
            owner.is_channel_admin = True
            owner.save()




@receiver(post_delete, sender=Channel)
def handle_channel_delete(sender, instance, **kwargs):

    owner = instance.owner
    is_owner_somewhere = Channel.objects.filter(owner=owner).exists()
    is_admin_somewhere = Channel.objects.filter(admins=owner).exists()

    if not is_owner_somewhere and not is_admin_somewhere:
        owner.is_channel_admin = False
        owner.save()

    for admin in instance.admins.all():
        is_owner_somewhere = Channel.objects.filter(owner=admin).exists()
        is_admin_somewhere = Channel.objects.filter(admins=admin).exists()
        if not is_owner_somewhere and not is_admin_somewhere:
            admin.is_channel_admin = False
            admin.save()
