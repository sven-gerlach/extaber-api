"""Module for a view class for the join table called article_votes"""

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from ..serializers import ArticleVotesSerializer
from ..models.article_votes import ArticleVote

class ArticleVotes(generics.ListCreateAPIView):
    """
    A class for retrieving, updating, and destroying an instance of the
    ArticleVotes model class
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        """Index request"""
        # Get all the votes:
        votes = ArticleVote.objects.all()
        # Run the data through the serializer
        serialized_votes = ArticleVotesSerializer(votes, many=True)
        return Response({'votes': serialized_votes.data})

    def post(self, request):
        """Create a vote"""
        # Add user to request data object
        request.data['vote']['owner'] = request.user.id
        # Serialize/create article
        serialized_vote = ArticleVotesSerializer(data=request.data['vote'])
        # If the data is valid according to our serializer...
        if serialized_vote.is_valid():
            # Save the created article & send a response
            serialized_vote.save()
            return Response({'vote': serialized_vote.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(serialized_vote.errors, status=status.HTTP_400_BAD_REQUEST)

