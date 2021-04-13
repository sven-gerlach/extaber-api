"""Module contains all PostgreSQL models"""

from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Article(models.Model):
    """A model for articles written by a user"""
    headline = models.CharField(max_length=200)
    body = models.TextField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Article with headline: {self.headline}"

    def as_dict(self):
        """Returns dictionary version of Article model"""
        return {
            'pk': self.pk,
            'headline': self.headline,
            'body': self.body,
            'owner': self.owner
        }
