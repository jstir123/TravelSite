from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.dispatch import receiver

User_Model = auth.get_user_model()

# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return self.username


def user_directory_path(instance, filename):
    return 'profile_pics/user_{0}/{1}'.format(instance.user.id, filename)

class ProfilePicture(models.Model):

    user = models.OneToOneField(User_Model, related_name='profile_pic', on_delete=models.CASCADE)
    prof_pic = models.ImageField(upload_to=user_directory_path)
    upload_date = models.DateTimeField(default=timezone.now)


@receiver(models.signals.post_delete, sender=ProfilePicture)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `ProfilePicture` object is deleted.
    """
    if instance.prof_pic:
        if os.path.isfile(instance.prof_pic.path):
            os.remove(instance.prof_pic.path)

@receiver(models.signals.pre_save, sender=ProfilePicture)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `ProfilePicture` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = ProfilePicture.objects.get(pk=instance.pk).prof_pic
    except ProfilePicture.DoesNotExist:
        return False

    new_file = instance.prof_pic
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
