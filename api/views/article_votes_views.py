"""Module for a view class for the join table called article_votes"""

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from ..serializers import ArticleVotesSerializer
from ..models.article import Article
from ..models.article_votes import ArticleVote
from django.shortcuts import get_object_or_404

class ArticleVotes(generics.ListCreateAPIView):
    """
    A class for retrieving, creating an instance of the
    ArticleVote model class
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
        # Query article and check that article owner is not the same as the user
        # making the request -> this avoids creators voting up their own article
        article_id = request.data['vote']['article']
        article = get_object_or_404(Article, pk=article_id)
        if article.owner.id == request.user.id:
            raise PermissionDenied('You cannot vote on your own article.')

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


class ArticleVotesDetail(generics.RetrieveUpdateDestroyAPIView):
    """class for article specific http requests"""

    def get(self, request, pk):
        """Return net votes for article pk"""
        # Locate the article to show
        votes = ArticleVote.objects.all()

        # Filter votes for articles with pk
        filtered_votes = votes.filter(article=pk)

        # if there no articles matching that pk, return no content
        if len(filtered_votes) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # else, iterate over query set and return the net votes
        net_votes = 0

        for key in filtered_votes:
            net_votes += key.vote

        return Response({'net_votes': net_votes})

    def delete(self, request, pk):
        """Delete a vote with pk - purely needed for admin purposes"""
        vote = get_object_or_404(ArticleVote, pk=pk)
        if not request.user.id == vote.owner.id:
            raise PermissionDenied('Unauthorized, you are not the author of this vote!')
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
