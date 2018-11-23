from rest_framework import serializers

from comicsdb.models import Arc, Character, Credits, Issue, Publisher, Series, Role


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('name',)


class CreditsSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.name')
    slug = serializers.ReadOnlyField(source='creator.slug')
    role = RoleSerializer('role', many=True)

    class Meta:
        model = Credits
        fields = ('creator', 'slug', 'role')


class IssueArcSerializer(serializers.ModelSerializer):

    class Meta:
        model = Arc
        fields = ('name', 'slug')


class IssueCharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ('name', 'slug')


class IssueSerializer(serializers.ModelSerializer):
    credits = CreditsSerializer(
        source='credits_set', many=True, read_only=True)
    arcs = IssueArcSerializer(many=True, read_only=True)
    characters = IssueArcSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ('__str__', 'slug', 'name', 'number', 'cover_date',
                  'store_date', 'desc', 'arcs', 'image', 'credits', 'characters')
        lookup_field = 'slug'


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = ('name', 'slug', 'founded', 'desc', 'image')
        lookup_field = 'slug'


class SeriesImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True,
                                   allow_null=True, required=False)

    class Meta:
        model = Issue
        fields = ('image',)
        lookup_field = 'slug'


class SeriesSerializer(serializers.ModelSerializer):
    issue_count = serializers.ReadOnlyField
    image = SeriesImageSerializer(source='issue_set.first', many=False)
    series_type = serializers.ReadOnlyField(source='series_type.name')

    class Meta:
        model = Series
        fields = ('name', 'slug', 'sort_name', 'volume', 'series_type',
                  'year_began', 'year_end', 'desc', 'issue_count', 'image')
        lookup_field = 'slug'

    def to_representation(self, obj):
        """ Move image field from Issue to Series representation. """
        representation = super().to_representation(obj)
        issue_representation = representation.pop('image')
        for key in issue_representation:
            representation[key] = issue_representation[key]

        return representation
