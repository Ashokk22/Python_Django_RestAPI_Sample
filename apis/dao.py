from apis.models import Person, Title
from apis.serializers import PersonSerializer, TitleSerializer


def get_person(person_id):
    return PersonSerializer(Person.objects.get(pk=person_id)).data


def get_title(title_id):
    return TitleSerializer(Title.objects.get(pk=title_id)).data
