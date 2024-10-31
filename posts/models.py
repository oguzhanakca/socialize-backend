from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Post(models.Model):
    """
    Post model
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = CloudinaryField(
        'post_image', default='default_post_uu0i5n'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner} - {self.title}'
