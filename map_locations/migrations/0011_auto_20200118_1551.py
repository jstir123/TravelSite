# Generated by Django 2.2.8 on 2020-01-18 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_locations', '0010_tripimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripimages',
            name='image',
            field=models.ImageField(upload_to='trip_pics/'),
        ),
    ]