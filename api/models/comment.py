
"""A module for the PostgreSQL comment model"""

from django.db import models
from django.contrib.auth import get_user_model
from .article import Article


# Create your models here.
class Comment(models.Model):
    """A model for comments made by a user on a specific article"""
    body = models.TextField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article,
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.body

    def as_dict(self):
        """Returns dictionary version of Article model"""
        return {
            'pk': self.pk,
            'body': self.body,
            'owner': self.owner,
            'article': self.article
        }
