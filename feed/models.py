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