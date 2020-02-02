from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Following(models.Model):

    following_user = models.ForeignKey(User, related_name='following_user', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followed_user', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=True)

    class Meta():
        ordering = ['followed_user']
        unique_together = ['following_user','followed_user']

    def __str__(self):
        return str(self.following_user.first_name) + ' follows ' + str(self.followed_user.first_name)
