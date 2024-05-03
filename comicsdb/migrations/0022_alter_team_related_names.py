# Generated by Django 5.0.3 on 2024-03-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsdb', '0021_alter_character_creators_alter_character_teams_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='creators',
            field=models.ManyToManyField(blank=True, related_name='teams', to='comicsdb.creator'),
        ),
        migrations.AlterField(
            model_name='team',
            name='universes',
            field=models.ManyToManyField(blank=True, related_name='teams', to='comicsdb.universe'),
        ),
    ]