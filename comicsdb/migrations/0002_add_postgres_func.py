# Generated by Django 2.1.4 on 2018-12-21 14:33

from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comicsdb', '0001_initial'),
    ]

    operations = [
        UnaccentExtension(),
        TrigramExtension()
    ]