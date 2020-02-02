import os
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Trips(models.Model):

    traveler = models.ForeignKey(User, related_name='user_trips', on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30, blank=True)
    country = CountryField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=240, blank=True, null=True)
    latitude = models.DecimalField(max_digits=16, decimal_places=13)
    longitude = models.DecimalField(max_digits=16, decimal_places=13)

    def __str__(self):
        if self.state != '':
            return str(self.city) + ', ' + str(self.state)
        else:
            return str(self.city) + ', ' + str(self.country.name)

    def get_absolute_url(self):
        return reverse('map_locations:mytrips')

    class Meta:
        ordering = ['-start_date']
        unique_together = ['traveler', 'city', 'state','country', 'start_date']


def user_directory_path(instance, filename):
    return 'trip_pics/user_{0}/{1}'.format(instance.trip.traveler.id, filename)

class TripImages(models.Model):

    trip = models.ForeignKey(Trips, related_name='trip_photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
    upload_date = models.DateTimeField(default=timezone.now)


@receiver(models.signals.post_delete, sender=TripImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `ProfilePicture` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
