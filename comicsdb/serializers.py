from rest_framework import serializers

from comicsdb.models import Publisher, Series, Issue


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
    series_type = serializers.CharField(source='series_type.name')

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
