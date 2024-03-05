# Generated by Django 5.0.2 on 2024-03-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0023_alter_statistic_captured_stones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='captured_stones',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='territory_points',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]