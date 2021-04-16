"""
A module for a model class of votes, representing the join table of the
many-to-many relationship between Users and Articles. One user can give many
articles an up or down-vote. One article can receive many up- or down-votes
from many users.
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


class CommentVote(models.Model):
    """
    A class representing join table, recording all comment votes cast
    by users.
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    vote = models.IntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(1)])

    def __str__(self):
        return self.vote
