# Generated by Django 4.0.4 on 2022-05-06 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_squashed_0006_alter_customuser_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="bio",
            field=models.TextField(blank=True),
        ),
    ]