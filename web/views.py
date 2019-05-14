from django.shortcuts import render

from apis.dao import get_person, get_title


def navigate(request, slug):
    return render(request, '%s.html' % slug, None)


def person(request, pk):
    person_data = get_person(pk)
    return render(request, 'person.html', person_data)


def title(request, pk):
    title_data = get_title(pk)
    return render(request, 'title.html', title_data)
