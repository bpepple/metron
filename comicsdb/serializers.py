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

    def create(self, validated_data):
        """
        Create and return a new `Arc` instance, given the validated data.
        """
        return Arc.objects.create(**validated_data)

    def update(self, instance: Arc, validated_data):
        """
        Update and return an existing `Arc` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance

    class Meta:
        model = Arc
        fields = ("id", "name", "desc", "image", "resource_url", "modified")


class CharacterSerializer(serializers.ModelSerializer):
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Character) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def create(self, validated_data):
        """
        Create and return a new `Character` instance, given the validated data.
        """
        creators_data = validated_data.pop("creators", None)
        teams_data = validated_data.pop("teams", None)
        character = Character.objects.create(**validated_data)
        if creators_data:
            for creator in creators_data:
                character.creators.add(creator)
        if teams_data:
            for team in teams_data:
                character.teams.add(team)
        return character

    def update(self, instance: Character, validated_data):
        """
        Update and return an existing `Character` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.image = validated_data.get("image", instance.image)
        instance.alias = validated_data.get("alias", instance.alias)
        if creators_data := validated_data.get("creators", None):
            for creator in creators_data:
                instance.creators.add(creator)
        if teams_data := validated_data.get("teams", None):
            for team in teams_data:
                instance.teams.add(team)
        instance.save()
        return instance

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


class CharacterReadSerializer(CharacterSerializer):
    creators = CreatorListSerializer(many=True, read_only=True)
    teams = TeamListSerializer(many=True, read_only=True)


class CreatorSerializer(serializers.ModelSerializer):
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Creator) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def create(self, validated_data):
        """
        Create and return a new `Creator` instance, given the validated data.
        """
        return Creator.objects.create(**validated_data)

    def update(self, instance: Creator, validated_data):
        """
        Update and return an existing `Character` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.image = validated_data.get("image", instance.image)
        instance.alias = validated_data.get("alias", instance.alias)
        instance.birth = validated_data.get("birth", instance.birth)
        instance.death = validated_data.get("death", instance.death)
        return instance

    class Meta:
        model = Creator
        fields = (
            "id",
            "name",
            "birth",
            "death",
            "desc",
            "image",
            "alias",
            "resource_url",
            "modified",
        )


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

    def create(self, validated_data):
        """
        Create and return a new `Publisher` instance, given the validated data.
        """
        return Publisher.objects.create(**validated_data)

    def update(self, instance: Publisher, validated_data):
        """
        Update and return an existing `Publisher` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.founded = validated_data.get("founded", instance.founded)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance

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
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Series) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def create(self, validated_data):
        """
        Create and return a new `Series` instance, given the validated data.
        """
        genres_data = validated_data.pop("genres", None)
        assoc_data = validated_data.pop("associated", None)
        series = Series.objects.create(**validated_data)
        if genres_data:
            for g in genres_data:
                series.genres.add(g)
        if assoc_data:
            for a in assoc_data:
                series.associated.add(a)

        return series

    def update(self, instance: Series, validated_data):
        """
        Update and return an existing `Series` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.sort_name = validated_data.get("sort_name", instance.sort_name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.volume = validated_data.get("volume", instance.volume)
        instance.year_began = validated_data.get("year_began", instance.year_began)
        instance.year_end = validated_data.get("year_end", instance.year_end)
        instance.series_type = validated_data.get("series_type", instance.series_type)
        instance.publisher = validated_data.get("publisher", instance.publisher)
        if genres_data := validated_data.pop("genres", None):
            for g in genres_data:
                instance.genres.add(g)
        if assoc_data := validated_data.pop("associated", None):
            for a in assoc_data:
                instance.associated.add(a)
        instance.save()
        return instance

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
            "genres",
            "associated",
            "resource_url",
            "modified",
        )


class SeriesReadSerializer(SeriesSerializer):
    publisher = IssuePublisherSerializer(read_only=True)
    series_type = SeriesTypeSerializer(read_only=True)
    issue_count = serializers.ReadOnlyField
    associated = AssociatedSeriesSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)


class TeamSerializer(serializers.ModelSerializer):
    creators = CreatorListSerializer(many=True, read_only=True)
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Team) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def create(self, validated_data):
        """
        Create and return a new `Team` instance, given the validated data.
        """
        creators_data = validated_data.pop("creators", None)
        team = Team.objects.create(**validated_data)
        if creators_data:
            for creator in creators_data:
                team.creators.add(creator)

        return team

    def update(self, instance: Team, validated_data):
        """
        Update and return an existing `Team` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.image = validated_data.get("image", instance.image)
        if creators_data := validated_data.pop("creators", None):
            for creator in creators_data:
                instance.creators.add(creator)
        instance.save()
        return instance

    class Meta:
        model = Team
        fields = ("id", "name", "desc", "image", "creators", "resource_url", "modified")


class TeamReadSerializer(TeamSerializer):
    creators = CreatorSerializer(many=True, read_only=True)
