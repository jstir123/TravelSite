# Generated by Django 2.2.8 on 2019-12-28 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_locations', '0008_auto_20191228_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='description',
            field=models.TextField(blank=True, max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='trips',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trips',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
