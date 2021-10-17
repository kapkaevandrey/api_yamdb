import os
import csv

from chardet import detect
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from api_yamdb import settings
from reviews.models import (Comment,
                            Category,
                            Genre,
                            GenreTitle,
                            Title,
                            Review)

User = get_user_model()


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

    def check_that_all_files_exists(self) -> None:
        """Проверяет наличие необходимых файлов в директории."""
        for file in Command.FILE_NAMES:
            if not os.path.exists(file):
                raise CommandError(f'"{file}" not exist in dir {os.getcwd()} ')
            self.stdout.write(self.style.SUCCESS(f'File {file} is exists.'))

    @staticmethod
    def go_to_dir_with_data_files() -> None:
        """Переходит в директорию где должны хранится файлы для заполнения из БД.
        По умолчанию: ~/static/data"""
        os.chdir(settings.BASE_DIR)
        os.chdir("...")
        os.chdir(os.path.join(os.getcwd(), "static\\data"))

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

    @classmethod
    def load_data_from_csv_in_db(cls):
        Command.load_data_category()
        Command.load_data_genre()
        Command.load_data_titles()
        Command.load_data_users()
        Command.load_data_review()
        Command.load_data_comments()
        Command.load_data_genre_titles()

    @staticmethod
    def load_data_category():
        reader = Command.get_file_reader("category.csv")
        for row in reader:
            Category.objects.create(
                pk=row['id'],
                name=row['name'],
                slug=row['slug']
            )

    @staticmethod
    def load_data_genre():
        reader = Command.get_file_reader("genre.csv")
        for row in reader:
            Genre.objects.create(
                pk=row['id'],
                name=row['name'],
                slug=row['slug']
            )

    @staticmethod
    def load_data_titles():
        reader = Command.get_file_reader("titles.csv")
        for row in reader:
            Title.objects.create(
                pk=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category_id']
            )

    @staticmethod
    def load_data_users():
        reader = Command.get_file_reader("users.csv")
        for row in reader:
            User.objects.create(
                pk=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role']
            )

    @staticmethod
    def load_data_review():
        reader = Command.get_file_reader("review.csv")
        for row in reader:
            Review.objects.create(
                pk=row['id'],
                text=row['text'],
                score=row['score'],
                pub_date=row['pub_date'],
                title_id=row['title_id'],
                author_id=row['author_id']
            )

    @staticmethod
    def load_data_comments():
        reader = Command.get_file_reader("comments.csv")
        for row in reader:
            Comment.objects.create(
                pk=row['id'],
                text=row['text'],
                pub_date=row['pub_date'],
                review_id=row['review_id'],
                author_id=row['author']
            )

    @staticmethod
    def load_data_genre_titles():
        reader = Command.get_file_reader("genre_title.csv")
        for row in reader:
            GenreTitle.objects.create(
                pk=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id']
            )

    def handle(self, *args, **options):
        Command.go_to_dir_with_data_files()
        self.check_that_all_files_exists()
        try:
            Command.load_data_from_csv_in_db()
        except Exception as error:
            raise CommandError("Objects can create", error)
        self.stdout.write(self.style.SUCCESS('Date Base Update.'))
