# Generated by Django 5.0.2 on 2024-03-04 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0027_alter_stone_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stone',
            name='game',
        ),
    ]
