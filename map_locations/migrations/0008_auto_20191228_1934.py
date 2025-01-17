# Generated by Django 2.2.8 on 2019-12-28 19:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('map_locations', '0007_auto_20191228_1902'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trips',
            unique_together={('traveler', 'city', 'state', 'country', 'start_date')},
        ),
    ]
