# Generated by Django 5.0.2 on 2024-03-04 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0039_stone_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stone',
            name='color',
            field=models.BooleanField(default=False),
        ),
    ]
