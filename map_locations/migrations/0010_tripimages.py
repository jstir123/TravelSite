# Generated by Django 2.2.8 on 2020-01-13 23:32

from django.db import migrations, models
import django.db.models.deletion
import map_locations.models


class Migration(migrations.Migration):

    dependencies = [
        ('map_locations', '0009_auto_20191228_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='trip_pics/')),
                ('upload_date', models.DateTimeField(auto_now=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_photos', to='map_locations.Trips')),
            ],
        ),
    ]
