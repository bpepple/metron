from rest_framework import serializers

from comicsdb.models import (
    Arc,
    Character,
    Creator,
    Credits,
    Issue,
    Publisher,
    Role,
    Series,
    Team,
    Variant,
)


class IssuePublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name")


class IssueSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ("id", "name")


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
    class Meta:
        model = Issue
        fields = ("id", "__str__", "cover_date", "modified")


class PublisherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "modified")


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")


class SeriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ("id", "__str__", "modified")


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name", "modified")


class ArcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arc
        fields = ("id", "name", "desc", "image", "modified")


class CharacterSerializer(serializers.ModelSerializer):
    creators = CreatorListSerializer(many=True, read_only=True)
    teams = TeamListSerializer(many=True, read_only=True)

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
            "modified",
        )


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ("id", "name", "birth", "death", "desc", "image", "modified")


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
    volume = serializers.ReadOnlyField(source="series.volume")

    class Meta:
        model = Issue
        fields = (
            "id",
            "publisher",
            "series",
            "volume",
            "number",
            "name",
            "cover_date",
            "store_date",
            "price",
            "sku",
            "upc",
            "page",
            "desc",
            "image",
            "arcs",
            "credits",
            "characters",
            "teams",
            "variants",
            "modified",
        )


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "founded", "desc", "image", "modified")


class SeriesImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )

    class Meta:
        model = Issue
        fields = ("image",)


class AssociatedSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ("id", "__str__")


class SeriesSerializer(serializers.ModelSerializer):
    publisher = IssuePublisherSerializer(read_only=True)
    issue_count = serializers.ReadOnlyField
    image = SeriesImageSerializer(source="issue_set.first", many=False)
    type = serializers.CharField(source="get_type_display")
    associated = AssociatedSeriesSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = (
            "id",
            "name",
            "sort_name",
            "volume",
            "type",
            "publisher",
            "year_began",
            "year_end",
            "desc",
            "issue_count",
            "image",
            "associated",
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

    class Meta:
        model = Team
        fields = ("id", "name", "desc", "image", "creators", "modified")
