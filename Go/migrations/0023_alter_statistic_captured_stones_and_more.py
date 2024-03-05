# Generated by Django 5.0.2 on 2024-03-04 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0022_rename_first_player_statistic_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='captured_stones',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='duration',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='outcome',
            field=models.CharField(blank=True, choices=[('Victory', 'Victory'), ('Loss', 'Loss'), ('Tie', 'Tie')], max_length=7),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='territory_points',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]