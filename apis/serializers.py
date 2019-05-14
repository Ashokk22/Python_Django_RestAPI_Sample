from rest_framework import serializers

from apis.models import Person, Profession, Title, Genre, PersonProfession, PersonTitle, TitleGenre


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('title',)


class PersonSerializer(serializers.ModelSerializer):
    primary_professions = serializers.SerializerMethodField()
    known_titles = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'primary_name', 'birth_year', 'death_year', 'primary_professions', 'known_titles',)

    def get_primary_professions(self, obj):
        query_set = PersonProfession.objects.filter(person=obj)
        return [ProfessionSerializer(r.profession).data for r in query_set]

    def get_known_titles(self, obj):
        query_set = PersonTitle.objects.filter(person=obj)
        return [TitleSerializer(r.title).data for r in query_set]


class TitleSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'original_name', 'is_adult', 'start_year', 'end_year', 'runtime', 'genres',)

    def get_genres(self, obj):
        query_set = TitleGenre.objects.filter(title=obj)
        return [GenreSerializer(r.genre).data for r in query_set]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)
