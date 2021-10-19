import csv
import os
import pathlib

from chardet import detect
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from reviews.models import (Comment,
                            Category,
                            Genre,
                            GenreTitle,
                            Title,
                            Review)


User = get_user_model()


class Command(BaseCommand):
    FILES_AND_MODELS_NAME = {
        'category.csv': {'model_obj': Category},
        'genre.csv': {'model_obj': Genre},
        'titles.csv': {'model_obj': Title},
        'users.csv': {'model_obj': User},
        'genre_title.csv': {'model_obj': GenreTitle},
        'review.csv': {'model_obj': Review},
        'comments.csv': {'model_obj': Comment}
    }

    help = "This script update rating in DB models Title."

    def check_that_all_files_exists(self) -> None:
        """Проверяет наличие необходимых файлов в директории."""
        for file in Command.FILES_AND_MODELS_NAME:
            if not os.path.exists(file):
                raise CommandError(f'"{file}" not exist in dir {os.getcwd()} ')
            self.stdout.write(self.style.SUCCESS(f'File {file} is exists.'))

    @staticmethod
    def go_to_dir_with_data_files() -> None:
        """Переходит в директорию где должны хранится файлы для заполнения из БД.
        По умолчанию: ~/static/data"""
        os.chdir(settings.BASE_DIR)
        os.chdir("...")
        os.chdir(pathlib.Path.cwd() / 'static' / 'data')
        print(pathlib.Path.cwd() / 'static' / 'data')

    @staticmethod
    def detect_encoding(file) -> dict:
        with open(file, "rb") as f:
            return detect(f.read())

    @staticmethod
    def get_file_reader(file: str):
        encoding_info = Command.detect_encoding(file)
        with open(file, "r", encoding=encoding_info["encoding"]) as f:
            reader = list(csv.DictReader(f))
            if len(reader) == 0:
                raise CommandError("File is empty")
            return reader

    @staticmethod
    def load_data_from_csv():
        for file_name, data in Command.FILES_AND_MODELS_NAME.items():
            reader = Command.get_file_reader(file_name)
            model_object = data['model_obj']
            for row in reader:
                model_object.objects.create(**row)

    def handle(self, *args, **options):
        Command.go_to_dir_with_data_files()
        self.check_that_all_files_exists()
        try:
            Command.load_data_from_csv()
        except Exception as error:
            raise CommandError("Objects can create", error)
        self.stdout.write(self.style.SUCCESS('Date Base Update.'))
