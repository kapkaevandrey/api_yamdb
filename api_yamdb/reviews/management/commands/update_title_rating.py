from django.core.management.base import BaseCommand, CommandError

from reviews.models import Titles


class Command(BaseCommand):
    help = "This script update rating in DB models Title."

    def handle(self, *args, **options):
        try:
            titles = Titles.objects.all()
        except Titles.DoesNotExist:
            raise CommandError("Object Titles is not exists")

        for title in titles:
            reviews_number = title.reviews.count()
            if reviews_number == 0:
                title.rating = None
            else:
                current_ratio = (
                        sum(review.score for review in title.reviews.all())
                        / reviews_number)
                title.rating = int(current_ratio)
            title.save()

        self.stdout.write(self.style.SUCCESS('Rating successful update.'))
