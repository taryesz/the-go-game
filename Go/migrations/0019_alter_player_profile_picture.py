# Generated by Django 5.0.2 on 2024-03-04 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0018_player_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_user_pfp.png', null=True, upload_to=''),
        ),
    ]
