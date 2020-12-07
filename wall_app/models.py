from django.db import models


# Create your models here.

class WallPost(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='wall_post', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']



