import csv
import json
import os
import re


def construct_fixture(dir_path, fixture_out_path, limit):
    """
    Constructs fixture file for movies app.

    :param dir_path: path to directory where the IMDB files are
    :param fixture_out_path: path to directory where the fixture file will be generated
    :param limit: number of names to fetch from IMDB file
    :return:
    """
    names_file = os.path.join(dir_path, "name.basics.tsv")
    titles_file = os.path.join(dir_path, "title.basics.tsv")
    person_list, titles_to_fetch = _load_names(names_file, limit)
    title_list = _load_titles(titles_file, titles_to_fetch)

    title_fixture = []
    genre_fixture = []
    title_genre_fixture = []
    genre_id_map = {}
    genre_db_id = 1
    title_genre_db_id = 1

    for title in title_list:
        title_id = title[0]
        # title structure: imdb_ref, original_name, is_adult, start_year, end_year, runtime, genres
        title_fixture.append(
            {
                "model": "apis.title",
                "pk": title_id,
                "fields": {
                    "original_name": title[1],
                    "is_adult": title[2],
                    "start_year": title[3],
                    "end_year": title[4],
                    "runtime": title[5]
                }
            }
        )

        for genre in title[6]:
            if genre not in genre_id_map:
                genre_id_map[genre] = genre_db_id
                genre_fixture.append(
                    {
                        "model": "apis.genre",
                        "pk": genre_db_id,
                        "fields": {
                            "name": genre
                        }
                    }
                )
                genre_db_id += 1
            title_genre_fixture.append(
                {
                    "model": "apis.titlegenre",
                    "pk": title_genre_db_id,
                    "fields": {
                        "title": title_id,
                        "genre": genre_id_map[genre],
                    }
                }
            )
            title_genre_db_id += 1

    person_fixture = []
    profession_fixture = []
    person_profession_fixture = []
    person_title_fixture = []
    profession_id_map = {}
    profession_db_id = 1
    person_profession_db_id = 1
    person_title_db_id = 1

    for person in person_list:
        # person structure: imdb_ref, primary_name, birth_year, death_year, primary_professions, known_titles
        person_id = person[0]
        person_fixture.append(
            {
                "model": "apis.person",
                "pk": person_id,
                "fields": {
                    "primary_name": person[1],
                    "birth_year": person[2],
                    "death_year": person[3]
                }
            }
        )
        for profession in person[4]:
            if profession not in profession_id_map:
                profession_id_map[profession] = profession_db_id
                profession_fixture.append(
                    {
                        "model": "apis.profession",
                        "pk": profession_db_id,
                        "fields": {
                            "title": profession
                        }
                    }
                )
                profession_db_id += 1
            person_profession_fixture.append(
                {
                    "model": "apis.personprofession",
                    "pk": person_profession_db_id,
                    "fields": {
                        "person": person_id,
                        "profession": profession_id_map[profession],
                    }
                }
            )
            person_profession_db_id += 1
        for title_id in person[5]:
            person_title_fixture.append(
                {
                    "model": "apis.persontitle",
                    "pk": person_title_db_id,
                    "fields": {
                        "person": person_id,
                        "title": title_id,
                    }
                }
            )
            person_title_db_id += 1

    with open(os.path.join(fixture_out_path, "movies.json"), "w") as out_file:
        out_file.write(json.dumps(
            person_fixture + profession_fixture + person_profession_fixture + title_fixture + genre_fixture + title_genre_fixture + person_title_fixture))


def _load_names(names_file_path, limit):
    """
    Reads the first `limit` number of records from imdb names file and list of names and their associated known titles.

    :param names_file_path: path to directory containing names and titles files downloaded from IMDB.
    :param limit: number of names to fetch
    :return: a tuple containing list of names and set of all known titles associated with the names
    """
    # name.basics.tsv
    # title.basics.tsv
    person_list = []  # structure: imdb_ref, primary_name, birth_year, death_year, primary_professions
    titles_to_fetch = set()

    with open(names_file_path) as in_file:
        reader = csv.reader(in_file, delimiter='\t')
        next(reader)  # skip header line
        for i in range(1, limit + 1):
            try:
                row = next(reader)
                # Row structure
                # nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles
                imdb_ref = int(row[0][2:])  # strip `nm` from imdb ref (ex: nm0000014) so we could save them as integers
                primary_name = row[1]
                birth_year = int(row[2]) if re.match(r"^\d+$", row[2]) else None
                death_year = int(row[3]) if re.match(r"^\d+$", row[3]) else None
                primary_professions = row[4].split(",") if row[4] else []
                known_titles = [int(_id[2:]) for _id in row[5].split(",")] if row[5] else []
                titles_to_fetch.update(known_titles)
                person_list.append((imdb_ref, primary_name, birth_year, death_year, primary_professions, known_titles))
            except StopIteration:
                # lines in file exhausted before limit
                pass
    return person_list, titles_to_fetch


def _load_titles(titles_file_path, titles_to_fetch):
    """
    Fetches the titles from the IMDB titles file.

    :param titles_file_path: IMDB titles file path
    :param titles_to_fetch: collection of title IDs to fetch
    :return: list of title records
    """
    with open(titles_file_path) as in_file:
        reader = csv.reader(in_file, delimiter='\t')
        next(reader)  # skip header line
        title_list = []  # structure: imdb_ref, original_name, is_adult, start_year, end_year, runtime, genres
        for row in reader:
            # Row structure
            # tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres
            imdb_ref = int(row[0][2:])
            if imdb_ref in titles_to_fetch:
                original_name = row[3]
                is_adult = int(row[4])
                start_year = int(row[5])
                end_year = int(row[6]) if re.match(r"^\d+$", row[6]) else None
                runtime = int(row[7]) if re.match(r"^\d+$", row[7]) else 0
                genres = row[8].split(",") if row[8] else []
                title_list.append((imdb_ref, original_name, is_adult, start_year, end_year, runtime, genres,))
        return title_list


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--imdbfilesdir", help="Directory path to names and titles file", required=True)
    parser.add_argument("--fixturedir", help="Directory path to names and titles file", required=True)
    parser.add_argument("--limit", help="Number of names to load", type=int, required=True)
    args = parser.parse_args()

    if args.imdbfilesdir:
        construct_fixture(args.imdbfilesdir, args.fixturedir, args.limit)


# construct_fixture("/Users/lodiatif/Downloads", "/Users/lodiatif/Documents/workspace/movies/apis/fixtures", 3)