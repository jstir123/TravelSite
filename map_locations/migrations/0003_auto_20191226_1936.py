# Generated by Django 2.2.8 on 2019-12-26 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_locations', '0002_auto_20191224_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='latitude',
            field=models.DecimalField(decimal_places=13, max_digits=16),
        ),
        migrations.AlterField(
            model_name='trips',
            name='longitude',
            field=models.DecimalField(decimal_places=13, max_digits=16),
        ),
    ]