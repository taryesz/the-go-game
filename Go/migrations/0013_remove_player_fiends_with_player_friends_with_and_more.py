# Generated by Django 5.0.2 on 2024-03-03 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0012_player_dark_mode_player_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='fiends_with',
        ),
        migrations.AddField(
            model_name='player',
            name='friends_with',
            field=models.ManyToManyField(blank=True, related_name='friends', to='Go.player'),
        ),
        migrations.AlterField(
            model_name='player',
            name='language',
            field=models.CharField(choices=[('English', 'English'), ('Ukrainian', 'Ukrainian'), ('Polish', 'Polish')], default='English', max_length=15),
        ),
    ]
