# Generated by Django 5.0.3 on 2024-03-12 14:00

import django.contrib.postgres.fields
import django.contrib.postgres.operations
import django.db.models.deletion
import django.db.models.functions.datetime
import sorl.thumbnail.fields
from django.conf import settings
from django.db import migrations, models


def add_ratings(apps, schema_editor):
    rating_model = apps.get_model("comicsdb", "Rating")
    ratings = [
        rating_model(name="Unknown"),
        rating_model(name="Everyone", short_description="Appropriate for readers of all ages"),
        rating_model(
            name="Teen", short_description="Appropriate for readers age 12 and older"
        ),
        rating_model(
            name="Teen Plus", short_description="Appropriate for readers age 15 and older"
        ),
        rating_model(
            name="Mature", short_description="Appropriate for readers age 17 and older"
        ),
    ]
    rating_model.objects.bulk_create(ratings)


def remove_ratings(apps, schema_editor):
    rating_model = apps.get_model("comicsdb", "Rating")
    rating_model.objects.all().delete()


def add_initial_genres(apps, schema_editor):
    genres = [
        "Adult",
        "Espionage",
        "Fantasy",
        "Historical",
        "Horror",
        "Humor",
        "Manga",
        "Romance",
        "Science Fiction",
        "Super-Hero",
        "War",
        "Western",
    ]
    genre_model = apps.get_model("comicsdb", "Genre")
    for i in genres:
        genre_model.objects.create(name=i)


def migrate_wikipedia_field(apps, schema_editor):
    """
    Let's move existing wikipedia field data to attribution model.
    """
    attribution_model = apps.get_model("comicsdb", "Attribution")
    content_type_model = apps.get_model("contenttypes", "ContentType")

    character_model = apps.get_model("comicsdb", "Character")
    character_content_type = content_type_model.objects.get_for_model(character_model)
    for character in character_model.objects.all():
        if character.wikipedia:
            url = f"https://en.wikipedia.org/wiki/{character.wikipedia}"
            attribution_model.objects.create(
                object_id=character.id,
                content_type=character_content_type,
                source="W",
                url=url,
            )

    creator_model = apps.get_model("comicsdb", "Creator")
    creator_content_type = content_type_model.objects.get_for_model(creator_model)
    for creator in creator_model.objects.all():
        if creator.wikipedia:
            url = f"https://en.wikipedia.org/wiki/{creator.wikipedia}"
            attribution_model.objects.create(
                object_id=creator.id, content_type=creator_content_type, source="W", url=url
            )

    publisher_model = apps.get_model("comicsdb", "Publisher")
    publisher_content_type = content_type_model.objects.get_for_model(publisher_model)
    for publisher in publisher_model.objects.all():
        if publisher.wikipedia:
            url = f"https://en.wikipedia.org/wiki/{publisher.wikipedia}"
            attribution_model.objects.create(
                object_id=publisher.id,
                content_type=publisher_content_type,
                source="W",
                url=url,
            )

    team_model = apps.get_model("comicsdb", "Team")
    team_content_type = content_type_model.objects.get_for_model(team_model)
    for team in team_model.objects.all():
        if team.wikipedia:
            url = f"https://en.wikipedia.org/wiki/{team.wikipedia}"
            attribution_model.objects.create(
                object_id=team.id, content_type=team_content_type, source="W", url=url
            )


class Migration(migrations.Migration):
    replaces = []

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        django.contrib.postgres.operations.UnaccentExtension(),
        django.contrib.postgres.operations.TrigramExtension(),
        migrations.CreateModel(
            name="Arc",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                ("modified", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(blank=True, upload_to="arc/%Y/%m/%d/"),
                ),
                (
                    "edited_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Character",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                ("modified", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "wikipedia",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Wikipedia Slug"
                    ),
                ),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(
                        blank=True, upload_to="character/%Y/%m/%d/"
                    ),
                ),
                (
                    "alias",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Creator",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                ("modified", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "wikipedia",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Wikipedia Slug"
                    ),
                ),
                (
                    "birth",
                    models.DateField(blank=True, null=True, verbose_name="Date of Birth"),
                ),
                (
                    "death",
                    models.DateField(blank=True, null=True, verbose_name="Date of Death"),
                ),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(
                        blank=True, upload_to="creator/%Y/%m/%d/"
                    ),
                ),
                (
                    "alias",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "edited_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Credits",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="comicsdb.creator"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Credits",
                "ordering": ["issue", "creator__name"],
            },
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                ("modified", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "name",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            max_length=150, verbose_name="Story Title"
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("number", models.CharField(max_length=25)),
                ("cover_date", models.DateField(verbose_name="Cover Date")),
                (
                    "store_date",
                    models.DateField(blank=True, null=True, verbose_name="In Store Date"),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        verbose_name="Cover Price",
                    ),
                ),
                (
                    "sku",
                    models.CharField(blank=True, max_length=9, verbose_name="Distributor SKU"),
                ),
                ("upc", models.CharField(blank=True, max_length=20, verbose_name="UPC Code")),
                (
                    "page",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Page Count"
                    ),
                ),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(
                        blank=True, upload_to="issue/%Y/%m/%d/", verbose_name="Cover"
                    ),
                ),
                ("arcs", models.ManyToManyField(blank=True, to="comicsdb.arc")),
                ("characters", models.ManyToManyField(blank=True, to="comicsdb.character")),
                (
                    "created_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "creators",
                    models.ManyToManyField(
                        blank=True, through="comicsdb.Credits", to="comicsdb.creator"
                    ),
                ),
                (
                    "edited_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        related_name="editor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["series__sort_name", "cover_date", "store_date", "number"],
            },
        ),
        migrations.CreateModel(
            name="Publisher",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                ("modified", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "founded",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Year Founded"
                    ),
                ),
                (
                    "wikipedia",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Wikipedia Slug"
                    ),
                ),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(
                        blank=True, upload_to="publisher/%Y/%m/%d/", verbose_name="Logo"
                    ),
                ),
                (
                    "edited_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=25)),
                ("order", models.PositiveSmallIntegerField(unique=True)),
                ("notes", models.TextField(blank=True)),
                ("modified", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="SeriesType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("notes", models.TextField(blank=True)),
                ("modified", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Variant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(
                        upload_to="variants/%Y/%m/%d/", verbose_name="Variant Cover"
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, verbose_name="Name")),
                (
                    "sku",
                    models.CharField(blank=True, max_length=9, verbose_name="Distributor SKU"),
                ),
                ("upc", models.CharField(blank=True, max_length=20, verbose_name="UPC Code")),
                (
                    "issue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="comicsdb.issue"
                    ),
                ),
            ],
            options={
                "ordering": ["issue"],
            },
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                ("modified", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "wikipedia",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Wikipedia Slug"
                    ),
                ),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(blank=True, upload_to="team/%Y/%m/%d/"),
                ),
                ("creators", models.ManyToManyField(blank=True, to="comicsdb.creator")),
                (
                    "edited_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Series",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                ("modified", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("sort_name", models.CharField(max_length=255)),
                ("volume", models.PositiveSmallIntegerField(verbose_name="Volume Number")),
                ("year_began", models.PositiveSmallIntegerField(verbose_name="Year Began")),
                (
                    "year_end",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Year Ended"
                    ),
                ),
                ("associated", models.ManyToManyField(blank=True, to="comicsdb.series")),
                (
                    "edited_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "publisher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="comicsdb.publisher"
                    ),
                ),
                (
                    "series_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="comicsdb.seriestype"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Series",
                "ordering": ["sort_name", "year_began"],
                "unique_together": {("publisher", "name", "volume", "series_type")},
            },
        ),
        migrations.AddField(
            model_name="issue",
            name="series",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="comicsdb.series"
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="teams",
            field=models.ManyToManyField(blank=True, to="comicsdb.team"),
        ),
        migrations.AddField(
            model_name="credits",
            name="issue",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="comicsdb.issue"
            ),
        ),
        migrations.AddField(
            model_name="credits",
            name="role",
            field=models.ManyToManyField(to="comicsdb.role"),
        ),
        migrations.AddField(
            model_name="character",
            name="creators",
            field=models.ManyToManyField(blank=True, to="comicsdb.creator"),
        ),
        migrations.AddField(
            model_name="character",
            name="edited_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="teams",
            field=models.ManyToManyField(blank=True, to="comicsdb.team"),
        ),
        migrations.AlterUniqueTogether(
            name="issue",
            unique_together={("series", "number")},
        ),
        migrations.AlterUniqueTogether(
            name="credits",
            unique_together={("issue", "creator")},
        ),
        migrations.CreateModel(
            name="Attribution",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[("M", "Marvel"), ("W", "Wikipedia")],
                        default="W",
                        max_length=1,
                    ),
                ),
                ("url", models.URLField()),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "ordering": ["content_type", "object_id"],
            },
        ),
        migrations.RunPython(
            code=migrate_wikipedia_field,
        ),
        migrations.RemoveField(
            model_name="character",
            name="wikipedia",
        ),
        migrations.RemoveField(
            model_name="creator",
            name="wikipedia",
        ),
        migrations.RemoveField(
            model_name="publisher",
            name="wikipedia",
        ),
        migrations.RemoveField(
            model_name="team",
            name="wikipedia",
        ),
        migrations.AlterUniqueTogether(
            name="attribution",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="attribution",
            name="source",
            field=models.CharField(
                choices=[("M", "Marvel"), ("W", "Wikipedia"), ("G", "Grand Comics Database")],
                default="W",
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="reprints",
            field=models.ManyToManyField(blank=True, to="comicsdb.issue"),
        ),
        migrations.AlterModelOptions(
            name="arc",
            options={},
        ),
        migrations.AlterModelOptions(
            name="character",
            options={},
        ),
        migrations.AlterModelOptions(
            name="creator",
            options={},
        ),
        migrations.AlterModelOptions(
            name="publisher",
            options={},
        ),
        migrations.AlterModelOptions(
            name="team",
            options={},
        ),
        migrations.AddIndex(
            model_name="arc",
            index=models.Index(fields=["name"], name="arc_name_idx"),
        ),
        migrations.AddIndex(
            model_name="attribution",
            index=models.Index(fields=["content_type", "object_id"], name="ct_obj_id_idx"),
        ),
        migrations.AddIndex(
            model_name="character",
            index=models.Index(fields=["name"], name="character_name_idx"),
        ),
        migrations.AddIndex(
            model_name="creator",
            index=models.Index(fields=["name"], name="creator_name_idx"),
        ),
        migrations.AddIndex(
            model_name="credits",
            index=models.Index(fields=["issue", "creator"], name="issue_creator_idx"),
        ),
        migrations.AddIndex(
            model_name="issue",
            index=models.Index(
                fields=["series", "cover_date", "store_date", "number"],
                name="series_cover_store_num_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="publisher",
            index=models.Index(fields=["name"], name="publisher_name_idx"),
        ),
        migrations.AddIndex(
            model_name="series",
            index=models.Index(fields=["sort_name", "year_began"], name="sort_year_began_idx"),
        ),
        migrations.AddIndex(
            model_name="series",
            index=models.Index(fields=["name"], name="series_name_idx"),
        ),
        migrations.AddIndex(
            model_name="team",
            index=models.Index(fields=["name"], name="team_name_idx"),
        ),
        migrations.AddIndex(
            model_name="variant",
            index=models.Index(fields=["issue"], name="issue_idx"),
        ),
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
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=25)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                ("modified", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="series",
            name="genres",
            field=models.ManyToManyField(blank=True, to="comicsdb.genre"),
        ),
        migrations.RunPython(
            code=add_initial_genres,
        ),
        migrations.AddField(
            model_name="issue",
            name="title",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Collection Title"
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="isbn",
            field=models.CharField(blank=True, max_length=13, verbose_name="ISBN"),
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("short_description", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.RunPython(
            code=add_ratings,
            reverse_code=remove_ratings,
        ),
        migrations.AddField(
            model_name="issue",
            name="rating",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="comicsdb.rating",
            ),
        ),
        migrations.AddIndex(
            model_name="issue",
            index=models.Index(fields=["series", "number"], name="series_number_idx"),
        ),
        migrations.AddField(
            model_name="arc",
            name="cv_id",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Comic Vine ID"
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="cv_id",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Comic Vine ID"
            ),
        ),
        migrations.AddField(
            model_name="creator",
            name="cv_id",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Comic Vine ID"
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="cv_id",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Comic Vine ID"
            ),
        ),
        migrations.AddField(
            model_name="publisher",
            name="cv_id",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Comic Vine ID"
            ),
        ),
        migrations.AddField(
            model_name="series",
            name="cv_id",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Comic Vine ID"
            ),
        ),
        migrations.AddField(
            model_name="team",
            name="cv_id",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Comic Vine ID"
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="cover_hash",
            field=models.CharField(blank=True, max_length=16, verbose_name="Cover Hash"),
        ),
        migrations.AlterField(
            model_name="arc",
            name="created_on",
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
        migrations.AlterField(
            model_name="character",
            name="created_on",
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
        migrations.AlterField(
            model_name="creator",
            name="created_on",
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
        migrations.AlterField(
            model_name="issue",
            name="created_on",
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
        migrations.AlterField(
            model_name="publisher",
            name="created_on",
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
        migrations.AlterField(
            model_name="series",
            name="created_on",
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
        migrations.AlterField(
            model_name="team",
            name="created_on",
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
        migrations.CreateModel(
            name="Universe",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("desc", models.TextField(blank=True, verbose_name="Description")),
                (
                    "cv_id",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Comic Vine ID"
                    ),
                ),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "created_on",
                    models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
                ),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(
                        blank=True, upload_to="universe/%Y/%m/%d/"
                    ),
                ),
                ("designation", models.CharField(blank=True, max_length=255)),
                (
                    "edited_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "publisher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="comicsdb.publisher"
                    ),
                ),
            ],
            options={
                "db_table_comment": "Publisher Universes",
                "ordering": ["name", "designation"],
                "indexes": [models.Index(fields=["name"], name="universe_name_idx")],
                "unique_together": {("publisher", "name", "designation")},
            },
        ),
        migrations.AddField(
            model_name="character",
            name="universes",
            field=models.ManyToManyField(blank=True, to="comicsdb.universe"),
        ),
        migrations.AddField(
            model_name="issue",
            name="universes",
            field=models.ManyToManyField(blank=True, to="comicsdb.universe"),
        ),
        migrations.AddField(
            model_name="team",
            name="universes",
            field=models.ManyToManyField(blank=True, to="comicsdb.universe"),
        ),
        migrations.AddField(
            model_name="series",
            name="collection",
            field=models.BooleanField(
                db_default=False,
                help_text="Whether a series has a collection title. Normally this only applies to Trade Paperbacks.",
                verbose_name="Allow Collection Title",
            ),
        ),
    ]
