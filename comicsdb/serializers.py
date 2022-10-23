from rest_framework import serializers

from comicsdb.models import (
    Arc,
    Character,
    Creator,
    Credits,
    Genre,
    Issue,
    Publisher,
    Rating,
    Role,
    Series,
    SeriesType,
    Team,
    Variant,
)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class SeriesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesType
        fields = ("id", "name")


class IssuePublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name")


class IssueSeriesSerializer(serializers.ModelSerializer):
    series_type = SeriesTypeSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = ("id", "name", "sort_name", "volume", "series_type", "genres")


class ArcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arc
        fields = ("id", "name", "modified")


class CharacterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ("id", "name", "modified")


class CreatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ("id", "name", "modified")


class IssueListSerializer(serializers.ModelSerializer):
    issue = serializers.CharField(source="__str__")

    class Meta:
        model = Issue
        fields = ("id", "issue", "cover_date", "modified")


class PublisherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "modified")


class ReprintSerializer(serializers.ModelSerializer):
    issue = serializers.CharField(source="__str__")

    class Meta:
        model = Issue
        fields = ("id", "issue")


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")


class SeriesListSerializer(serializers.ModelSerializer):
    series = serializers.CharField(source="__str__")

    class Meta:
        model = Series
        fields = ("id", "series", "modified")


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name", "modified")


class ArcSerializer(serializers.ModelSerializer):
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Arc) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Arc
        fields = ("id", "name", "desc", "image", "resource_url", "modified")


class CharacterSerializer(serializers.ModelSerializer):
    creators = CreatorListSerializer(many=True, read_only=True)
    teams = TeamListSerializer(many=True, read_only=True)
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Character) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Character
        fields = (
            "id",
            "name",
            "alias",
            "desc",
            "image",
            "creators",
            "teams",
            "resource_url",
            "modified",
        )


class CreatorSerializer(serializers.ModelSerializer):
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Creator) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Creator
        fields = ("id", "name", "birth", "death", "desc", "image", "resource_url", "modified")


class CreditsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="creator.id")
    creator = serializers.ReadOnlyField(source="creator.name")
    role = RoleSerializer("role", many=True)

    class Meta:
        model = Credits
        fields = ("id", "creator", "role")


class VariantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ("name", "sku", "upc", "image")


class IssueSerializer(serializers.ModelSerializer):
    variants = VariantsSerializer(source="variant_set", many=True, read_only=True)
    credits = CreditsSerializer(source="credits_set", many=True, read_only=True)
    arcs = ArcListSerializer(many=True, read_only=True)
    characters = CharacterListSerializer(many=True, read_only=True)
    teams = TeamListSerializer(many=True, read_only=True)
    publisher = IssuePublisherSerializer(source="series.publisher", read_only=True)
    series = IssueSeriesSerializer(read_only=True)
    reprints = ReprintSerializer(many=True, read_only=True)
    rating = RatingSerializer(read_only=True)
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Issue) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Issue
        fields = (
            "id",
            "publisher",
            "series",
            "number",
            "title",
            "name",
            "cover_date",
            "store_date",
            "price",
            "rating",
            "sku",
            "isbn",
            "upc",
            "page",
            "desc",
            "image",
            "arcs",
            "credits",
            "characters",
            "teams",
            "reprints",
            "variants",
            "resource_url",
            "modified",
        )


class PublisherSerializer(serializers.ModelSerializer):
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Publisher) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Publisher
        fields = ("id", "name", "founded", "desc", "image", "resource_url", "modified")


class SeriesImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )

    class Meta:
        model = Issue
        fields = ("image",)


class AssociatedSeriesSerializer(serializers.ModelSerializer):
    series = serializers.CharField(source="__str__")

    class Meta:
        model = Series
        fields = ("id", "series")


class SeriesSerializer(serializers.ModelSerializer):
    publisher = IssuePublisherSerializer(read_only=True)
    issue_count = serializers.ReadOnlyField
    image = SeriesImageSerializer(source="issue_set.first", many=False)
    series_type = SeriesTypeSerializer(read_only=True)
    associated = AssociatedSeriesSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Series) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Series
        fields = (
            "id",
            "name",
            "sort_name",
            "volume",
            "series_type",
            "publisher",
            "year_began",
            "year_end",
            "desc",
            "issue_count",
            "image",
            "genres",
            "associated",
            "resource_url",
            "modified",
        )

    def to_representation(self, instance):
        """Move image field from Issue to Series representation."""
        representation = super().to_representation(instance)
        issue_representation = representation.pop("image")
        for key in issue_representation:
            representation[key] = issue_representation[key]

        return representation


class TeamSerializer(serializers.ModelSerializer):
    creators = CreatorListSerializer(many=True, read_only=True)
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Team) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        model = Team
        fields = ("id", "name", "desc", "image", "creators", "resource_url", "modified")
