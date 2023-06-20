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


class IssueListSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ("name", "volume", "year_began")


class IssueListSerializer(serializers.ModelSerializer):
    issue = serializers.CharField(source="__str__")
    series = IssueListSeriesSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = (
            "id",
            "series",
            "number",
            "issue",
            "cover_date",
            "image",
            "cover_hash",
            "modified",
        )


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
    issue_count = serializers.ReadOnlyField

    class Meta:
        model = Series
        fields = ("id", "series", "year_began", "issue_count", "modified")


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
        if "image" in validated_data and validated_data["image"] is not None:
            validated_data["image"] = validated_data["image"].seek(0)
        return Arc.objects.create(**validated_data)

    def update(self, instance: Arc, validated_data):
        """
        Update and return an existing `Arc` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.image = validated_data.get("image", instance.image)
        instance.cv_id = validated_data.get("cv_id", instance.cv_id)
        instance.save()
        return instance

    class Meta:
        model = Arc
        fields = ("id", "name", "desc", "image", "cv_id", "resource_url", "modified")


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
        if "image" in validated_data and validated_data["image"] is not None:
            validated_data["image"] = validated_data["image"].seek(0)
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
        instance.cv_id = validated_data.get("cv_id", instance.cv_id)
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
            "cv_id",
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
        if "image" in validated_data and validated_data["image"] is not None:
            validated_data["image"] = validated_data["image"].seek(0)
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
        instance.cv_id = validated_data.get("cv_id", instance.cv_id)
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
            "cv_id",
            "resource_url",
            "modified",
        )


class CreditSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """
        Create and return a new `Credits` instance, given the validated data.
        """
        roles_data = validated_data.pop("role", None)
        credit = Credits.objects.create(**validated_data)
        for role in roles_data:
            credit.role.add(role)
        return credit

    def update(self, instance: Credits, validated_data):
        """
        Update and return an existing `Credits` instance, given the validated data.
        """
        instance.issue = validated_data.get("issue", instance.issue)
        instance.creator = validated_data.get("creator", instance.creator)
        if roles_data := validated_data.pop("role", None):
            for role in roles_data:
                instance.role.add(role)
        instance.save()
        return instance

    class Meta:
        model = Credits
        fields = "__all__"


class CreditReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="creator.id")
    creator = serializers.ReadOnlyField(source="creator.name")
    role = RoleSerializer("role", many=True)

    class Meta:
        model = Credits
        fields = ("id", "creator", "role")


class VariantsIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ("name", "sku", "upc", "image")


# TODO: Refactor this so reuse Issue serializer for read-only also.
#       Need to handle variants & credits sets.
class IssueSerializer(serializers.ModelSerializer):
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Issue) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def create(self, validated_data):
        """
        Create and return a new `Issue` instance, given the validated data.
        """
        arcs_data = validated_data.pop("arcs", None)
        characters_data = validated_data.pop("characters", None)
        teams_data = validated_data.pop("teams", None)
        reprints_data = validated_data.pop("reprints", None)
        if "image" in validated_data and validated_data["image"] is not None:
            validated_data["image"] = validated_data["image"].seek(0)
        issue: Issue = Issue.objects.create(**validated_data)
        if arcs_data:
            for arc in arcs_data:
                issue.arcs.add(arc)
        if characters_data:
            for character in characters_data:
                issue.characters.add(character)
        if teams_data:
            for team in teams_data:
                issue.teams.add(team)
        if reprints_data:
            for reprint in reprints_data:
                issue.reprints.add(reprint)
        return issue

    def update(self, instance: Issue, validated_data):
        """
        Update and return an existing `Issue` instance, given the validated data.
        """
        instance.series = validated_data.get("series", instance.series)
        instance.number = validated_data.get("number", instance.number)
        instance.title = validated_data.get("title", instance.title)
        instance.name = validated_data.get("name", instance.name)
        instance.cover_date = validated_data.get("cover_date", instance.cover_date)
        instance.store_date = validated_data.get("store_date", instance.store_date)
        instance.price = validated_data.get("price", instance.price)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.sku = validated_data.get("sku", instance.sku)
        instance.isbn = validated_data.get("isbn", instance.isbn)
        instance.upc = validated_data.get("upc", instance.upc)
        instance.page = validated_data.get("page", instance.page)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.image = validated_data.get("image", instance.image)
        instance.cv_id = validated_data.get("cv_id", instance.cv_id)
        if arcs_data := validated_data.pop("arcs", None):
            for arc in arcs_data:
                instance.arcs.add(arc)
        if characters_data := validated_data.pop("characters", None):
            for character in characters_data:
                instance.characters.add(character)
        if teams_data := validated_data.pop("teams", None):
            for team in teams_data:
                instance.teams.add(team)
        if reprints_data := validated_data.pop("reprints", None):
            for reprint in reprints_data:
                instance.reprints.add(reprint)
        instance.save()
        return instance

    class Meta:
        model = Issue
        fields = (
            "id",
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
            "characters",
            "teams",
            "reprints",
            "cv_id",
            "resource_url",
        )


class IssueReadSerializer(serializers.ModelSerializer):
    variants = VariantsIssueSerializer(source="variant_set", many=True, read_only=True)
    credits = CreditReadSerializer(source="credits_set", many=True, read_only=True)
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
            "cover_hash",
            "arcs",
            "credits",
            "characters",
            "teams",
            "reprints",
            "variants",
            "cv_id",
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
        if "image" in validated_data and validated_data["image"] is not None:
            validated_data["image"] = validated_data["image"].seek(0)
        return Publisher.objects.create(**validated_data)

    def update(self, instance: Publisher, validated_data):
        """
        Update and return an existing `Publisher` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.founded = validated_data.get("founded", instance.founded)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.image = validated_data.get("image", instance.image)
        instance.cv_id = validated_data.get("cv_id", instance.cv_id)
        instance.save()
        return instance

    class Meta:
        model = Publisher
        fields = (
            "id",
            "name",
            "founded",
            "desc",
            "image",
            "cv_id",
            "resource_url",
            "modified",
        )


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
        instance.cv_id = validated_data.get("cv_id", instance.cv_id)
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
            "cv_id",
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
    resource_url = serializers.SerializerMethodField("get_resource_url")

    def get_resource_url(self, obj: Team) -> str:
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def create(self, validated_data):
        """
        Create and return a new `Team` instance, given the validated data.
        """
        creators_data = validated_data.pop("creators", None)
        if "image" in validated_data and validated_data["image"] is not None:
            validated_data["image"] = validated_data["image"].seek(0)
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
        instance.cv_id = validated_data.get("cv_id", instance.cv_id)
        if creators_data := validated_data.pop("creators", None):
            for creator in creators_data:
                instance.creators.add(creator)
        instance.save()
        return instance

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "desc",
            "image",
            "creators",
            "cv_id",
            "resource_url",
            "modified",
        )


class TeamReadSerializer(TeamSerializer):
    creators = CreatorListSerializer(many=True, read_only=True)


class VariantSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """
        Create and return a new `Variant` instance, given the validated data.
        """
        return Variant.objects.create(**validated_data)

    def update(self, instance: Variant, validated_data):
        """
        Update and return an existing `Variant` instance, given the validated data.
        """
        instance.issue = validated_data.get("issue", instance.issue)
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.sku = validated_data.get("sku", instance.sku)
        instance.upc = validated_data.get("upc", instance.upc)
        instance.save()
        return instance

    class Meta:
        model = Variant
        fields = "__all__"
