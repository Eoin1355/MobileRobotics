# Generated by Django 5.0 on 2023-12-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_teams_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='route',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
