# Generated by Django 5.1 on 2024-10-06 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../default_profile_wxoxmn', upload_to='images/avatars/'),
        ),
    ]
