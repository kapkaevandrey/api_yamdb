import os
import csv
import sys

from django.core.management.base import BaseCommand, CommandError

from api_yamdb import settings
from reviews.models import (Comment,
                            Category,
                            Genre,
                            GenreTitle,
                            Title,
                            Review)


class Command(BaseCommand):
    FILE_NAMES = ['category.csv',
                  'genre.csv',
                  'titles.csv',
                  'users.csv',
                  'genre_title.csv',
                  'review.csv',
                  'comments.csv'
                  ]

    help = "This script update rating in DB models Title."

    @staticmethod
    def check_that_all_files_exists() -> None:
        """Проверяет наличие необходимых файлов в директории."""
        for file in Command.FILE_NAMES:
            if not os.path.exists(file):
                raise CommandError(f'"{file}" not exist in dir {os.getcwd()} ')
            print("Success")

    @staticmethod
    def go_to_dir_with_data_files() -> None:
        """Переходит в директорию где должны хранится файлы для заполнения из БД.
        По умолчанию: ~/static/data"""
        os.chdir(settings.BASE_DIR)
        os.chdir("...")
        os.chdir(os.path.join(os.getcwd(), "static\\data"))

    def handle(self, *args, **options):
        Command.go_to_dir_with_data_files()
        Command.check_that_all_files_exists()
        self.stdout.write(self.style.SUCCESS('Date Base Update.'))

