"""Module for a view class for the join table called article_votes"""

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from ..serializers import CommentVotesSerializer
from ..models.comment_votes import CommentVote

class CommentVotes(generics.ListCreateAPIView):
    """
    A class for retrieving and creating an instance of the
    CommentVote model class
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        """Index request"""
        # Get all the votes:
        votes = CommentVote.objects.all()
        # Run the data through the serializer
        serialized_votes = CommentVotesSerializer(votes, many=True)
        return Response({'votes': serialized_votes.data})

    def post(self, request):
        """Create a vote"""
        # Add user to request data object
        request.data['vote']['owner'] = request.user.id
        # Serialize/create article
        serialized_vote = CommentVotesSerializer(data=request.data['vote'])
        # If the data is valid according to our serializer...
        if serialized_vote.is_valid():
            # Save the created article & send a response
            serialized_vote.save()
            return Response({'vote': serialized_vote.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(serialized_vote.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentVotesDetail(generics.RetrieveUpdateDestroyAPIView):
    """class for article specific http requests"""

    def get(self, request, pk):
        """Return net votes for comment pk"""
        # Locate the article to show
        votes = CommentVote.objects.all()

        # Filter votes for comments with pk
        filtered_votes = votes.filter(comment=pk)

        # if there no comments matching the pk, return no content
        if len(filtered_votes) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # else, iterate over query set and return the net votes
        net_votes = 0

        for key in filtered_votes:
            net_votes += key.vote

        return Response({'net_votes': net_votes})

