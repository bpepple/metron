# Generated by Django 4.0.4 on 2022-04-22 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comicsdb", "0002_indexes"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="arc",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="character",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="creator",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="publisher",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="team",
            options={"ordering": ["name"]},
        ),
    ]
