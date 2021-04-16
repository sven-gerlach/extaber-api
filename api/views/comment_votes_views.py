"""Module for a view class for the join table called article_votes"""

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from ..serializers import CommentVotesSerializer
from ..models.comment_votes import CommentVote
from ..models.comment import Comment

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
        # Query comment and check that comment owner is not the same as the user
        # making the request -> this avoids creators voting up their own comments
        comment_id = request.data['vote']['comment']
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.owner.id == request.user.id:
            raise PermissionDenied('You cannot vote on your own comment.')

        # check if user has already cast a vote on comment
        user_has_voted = CommentVote.objects.filter(
            owner=request.user.id,
            comment=comment_id
        )

        def _add_vote():
            """helper function that adds a vote"""
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

        if len(user_has_voted) == 1:
            # if user has cast a vote, check if the vote is in the same direction
            if user_has_voted.filter(vote=request.data['vote']['vote']):
                # if yes: return error saying that only one vote may be case
                if request.data['vote']['vote'] == 0:
                    raise PermissionDenied('You have already removed your vote.')
                else:
                    raise PermissionDenied('You may not cast more than one vote.')
            else:
                # if no: then remove old vote and add new one
                user_has_voted.delete()
                return _add_vote()
        else:
            return _add_vote()


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

