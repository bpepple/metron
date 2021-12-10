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
    SeriesType,
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


class SeriesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesType
        fields = ("id", "name")


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name", "modified")


class ArcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arc
        fields = ("id", "name", "desc", "modified")
        read_only_field = ("image",)

    # TODO: Need to handle uploading of ImageField.

    def create(self, validated_data):
        """
        Create and return a new `Arc` instance, given the validated data.
        """
        return Arc.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Arc` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.save()
        return instance


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
            "wikipedia",
            "creators",
            "teams",
            "modified",
        )
        read_only_field = ("image",)

    # TODO: Need to handle uploading of ImageField.

    def create(self, validated_data):
        """
        Create and return a new `Character` instance, given the validated data.
        """
        return Character.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Character` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.alias = validated_data.get("alias", instance.alias)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.wikipedia = validated_data.get("wikipedia", instance.wikipedia)
        instance.save()
        return instance


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ("id", "name", "birth", "death", "desc", "wikipedia", "image", "modified")


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
        fields = ("id", "name", "founded", "desc", "wikipedia", "image", "modified")


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
    issue_count = serializers.ReadOnlyField
    image = SeriesImageSerializer(source="issue_set.first", many=False)
    series_type = SeriesTypeSerializer(read_only=True)
    associated = AssociatedSeriesSerializer(many=True, read_only=True)

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
        fields = ("id", "name", "desc", "wikipedia", "image", "creators", "modified")
