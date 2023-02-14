import os

from csv import DictReader
from django.apps import apps
from django.core.management import BaseCommand

from reviews.models import (
    Categories,
    Comment,
    Genre,
    Title,
    Review,
    User,
)

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from *.csv"

    def handle(self, *args, **options):
        models = {**apps.all_models['reviews']}
        file_names = {
            'users': User,
            'category': Categories,
            'titles': Title,
            'genre': Genre,
            'genre_title': models['title_genre'],
            'review': Review,
            'comments': Comment,
        }
        # Список полей у которых необходимо изменить имя
        replace_field = [
            'author',
            'category',
        ]

        for file in file_names:
            if file_names[file].objects.exists():
                print(f'{file} data already loaded...exiting.')
                print(ALREDY_LOADED_ERROR_MESSAGE)
                return
            print(f'Loading {file} data')
            directory = os.path.abspath('api_yamdb/static/data/')
            file_way = os.path.join(directory, file + '.csv')
            print(file_way)
            with open(file_way, encoding='utf-8') as csv_file:
                reader = DictReader(csv_file, delimiter=',')
                for index, field in enumerate(reader.fieldnames):
                    if field in replace_field:
                        reader.fieldnames[index] += '_id'
                for row in reader:
                    object, created = (
                        file_names[file].objects.get_or_create(**row)
                    )
                print(f'Loading {file} data completed')
