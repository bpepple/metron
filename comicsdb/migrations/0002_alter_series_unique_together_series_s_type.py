# Generated by Django 4.0.3 on 2022-03-12 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comicsdb", "0001_squashed_0007_issue_reprints"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="series",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="series",
            name="type",
            field=models.CharField(
                choices=[
                    ("AN", "Annual"),
                    ("CA", "Cancelled"),
                    ("GN", "Graphic Novel"),
                    ("HC", "Hard Cover"),
                    ("MX", "Maxi-Series"),
                    ("MN", "Mini-Series"),
                    ("OS", "One-Shot"),
                    ("OG", "Ongoing"),
                ],
                default="OG",
                max_length=2,
            ),
        ),
    ]
