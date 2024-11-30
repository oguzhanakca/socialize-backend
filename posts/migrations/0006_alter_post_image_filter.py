# Generated by Django 5.1 on 2024-10-06 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_image_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_filter',
            field=models.CharField(
                choices=[
                    ('normal', 'Normal'),
                    ('_1977', '1977'),
                    ('brannan', 'Brannan'),
                    ('earlybird', 'Earlybird'),
                    ('hudson', 'Hudson'),
                    ('inkwell', 'Inkwell'),
                    ('lofi', 'Lo-Fi'),
                    ('kelvin', 'Kelvin'),
                    ('nashville', 'Nashville'),
                    ('rise', 'Rise'),
                    ('toaster', 'Toaster'),
                    ('valencia', 'Valencia'),
                    ('walden', 'Walden'),
                    ('xpro2', 'X-pro II')
                ],
                default='normal',
                max_length=32
            ),
        ),
    ]
