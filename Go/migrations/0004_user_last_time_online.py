# Generated by Django 5.0.2 on 2024-03-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0003_remove_user_last_time_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_time_online',
            field=models.DateTimeField(auto_now=True),
        ),
    ]