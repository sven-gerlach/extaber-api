
"""A module for PostgreSQL article models"""

from django.db import models
from django.contrib.auth import get_user_model
from .article_votes import ArticleVote


# todo: consider using set() to persist articles beyond deletion of the user
# Create your models here.
class Article(models.Model):
    """A model for articles written by a user"""
    headline = models.CharField(max_length=200)
    body = models.TextField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    votes = models.ManyToManyField(
        get_user_model(),
        through=ArticleVote,
        through_fields=('article', 'owner'),
        related_name='+',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Article with headline: {self.headline}"

    def as_dict(self):
        """Returns dictionary version of Article model"""
        return {
            'pk': self.pk,
            'headline': self.headline,
            'body': self.body,
            'owner': self.owner,
            'votes': self.votes
        }
