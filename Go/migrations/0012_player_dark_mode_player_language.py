# Generated by Django 5.0.2 on 2024-03-02 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0011_alter_statistic_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='dark_mode',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='language',
            field=models.CharField(default='English', max_length=15),
        ),
    ]