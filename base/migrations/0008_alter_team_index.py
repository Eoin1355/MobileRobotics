# Generated by Django 5.0 on 2023-12-22 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_team_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='index',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
