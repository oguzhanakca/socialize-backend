from django.db import models
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    User Profile model
    Created automatically after account created
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = CloudinaryField(
        'profile_picture', default='default_profile_wxoxmn'
    )
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
