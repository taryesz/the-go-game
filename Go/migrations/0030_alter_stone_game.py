# Generated by Django 5.0.2 on 2024-03-04 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0029_stone_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stone',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Go.game'),
        ),
    ]