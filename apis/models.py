from django.db import models


class Profession(models.Model):
    title = models.CharField(max_length=50)


class Person(models.Model):
    primary_name = models.CharField(max_length=255)
    birth_year = models.IntegerField(null=True)
    death_year = models.IntegerField(null=True)
    # professions = models.ManyToManyField(Profession)


class PersonProfession(models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    profession = models.ForeignKey(to=Profession, on_delete=models.CASCADE)


class Title(models.Model):
    original_name = models.CharField(max_length=255)
    is_adult = models.BooleanField()
    start_year = models.IntegerField(null=True)
    end_year = models.IntegerField(null=True)
    runtime = models.IntegerField()
    genres = models.CharField(max_length=255)


class Genre(models.Model):
    name = models.CharField(max_length=30)


class TitleGenre(models.Model):
    title = models.ForeignKey(to=Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(to=Genre, on_delete=models.CASCADE)


class PersonTitle(models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    title = models.ForeignKey(to=Title, on_delete=models.CASCADE)
