# Generated by Django 3.2.7 on 2021-09-16 12:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comicsdb", "0001_squashed_0007_variant_sku"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalissue",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                default=1,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalissue",
            name="page",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="Page Count"
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="created_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="page",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="Page Count"
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="edited_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="editor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]