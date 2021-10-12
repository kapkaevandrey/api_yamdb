from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    title = models.IntegerField() # TODO заменить на FK когда модель Title будет написана
    pub_date = models.DateTimeField('Date of publication',
                                    auto_now_add=True,
                                    db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.IntegerField(default=1,
                                validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ])

    def __str__(self):
        return (f'Author - <{self.author}>; title - <{self.title}>'
                f'text part - <{self.text[:15]}>.')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique review'),
        ]
        ordering = ['-pub_date']



