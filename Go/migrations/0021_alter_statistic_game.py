# Generated by Django 5.0.2 on 2024-03-04 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0020_alter_game_board_size_alter_game_game_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Go.game'),
        ),
    ]