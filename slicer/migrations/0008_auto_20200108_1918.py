# Generated by Django 2.2.7 on 2020-01-08 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slicer', '0007_imageseries_png_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageseries',
            name='png_files',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
