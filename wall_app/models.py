from django.db import models


# Create your models here.

class WallPost(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    # owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    # highlighted = models.TextField()

    # def save(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     super(WallPost, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']



