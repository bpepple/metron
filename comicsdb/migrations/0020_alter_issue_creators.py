# Generated by Django 5.0.3 on 2024-03-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comicsdb", "0019_add_issues_related_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="creators",
            field=models.ManyToManyField(
                blank=True,
                related_name="issues",
                through="comicsdb.Credits",
                to="comicsdb.creator",
            ),
        ),
    ]
