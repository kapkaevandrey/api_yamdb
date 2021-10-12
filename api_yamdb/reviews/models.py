from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Date of publication',
                                    auto_now_add=True,
                                    db_index=True)
    score = models.PositiveSmallIntegerField(default=1,
                                             validators=[
                                                 MaxValueValidator(10),
                                                 MinValueValidator(1)
                                             ])
    title = models.IntegerField()  # TODO заменить на FK когда модель Title будет написана
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="reviews")

    def __str__(self):
        return (f'Author - <{self.author}>; title_id - <{self.title}>'
                f'review_id - <{self.id}> text part - <{self.text[:15]}>.')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique review'),
        ]
        ordering = ['-pub_date']


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Date of publication',
                                    auto_now_add=True,
                                    db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return (f'Author - <{self.author}>; review_id - <{self.review_id}>'
                f'comment_id - <{self.id}> text_part - <{self.text[:15]}>.')
