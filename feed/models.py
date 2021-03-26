from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Post(models.Model):
    body_text = models.CharField(max_length=240)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_posted = models.DateTimeField(auto_now_add=True)

    @property
    def post_id(self):
        return self.id

    @property
    def hue(self):
        hue = 0
        for vote in self.vote_set.all():
            hue += vote.hue # Not correct behaviour yet
        return hue

    def __str__(self):
        return self.author.username + ":" + self.body_text

class Vote(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    hue = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(360)]
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.post.id) + " " + self.author.username + " " + str(self.hue)