# Generated by Django 5.0.2 on 2024-03-02 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0010_rename_stats_statistic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='duration',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
