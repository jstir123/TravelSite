# Generated by Django 2.2.8 on 2019-12-26 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map_locations', '0005_auto_20191226_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='traveler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_trips', to=settings.AUTH_USER_MODEL),
        ),
    ]
