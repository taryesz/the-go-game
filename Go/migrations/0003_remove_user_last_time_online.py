# Generated by Django 5.0.2 on 2024-03-02 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0002_user_fiends_with'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_time_online',
        ),
    ]
