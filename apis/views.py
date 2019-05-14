from rest_framework import generics

from apis.models import Person, Title
from apis.serializers import PersonSerializer, TitleSerializer


class PersonList(generics.ListAPIView):
    serializer_class = PersonSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `name` query parameter in the URL.
        """
        queryset = Person.objects.all()
        person_name = self.kwargs.get('name')  # self.request.query_params.get('name', None)
        if person_name is not None:
            queryset = queryset.filter(primary_name__contains=person_name)
        return queryset


class PersonDetail(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class TitleDetail(generics.RetrieveAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
