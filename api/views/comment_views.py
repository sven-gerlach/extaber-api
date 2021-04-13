"""Module for comment views"""

from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from ..serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from ..models.comment import Comment


class Comments(generics.ListCreateAPIView):
    """A class for a PostgreSQL comment model"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """Index request for all comments associated with authorized user"""
        comment = Comment.objects.all().filter(owner=request.user.id)
        serialized_comment = CommentSerializer(comment, many=True)
        return Response({'comments': serialized_comment.data})

    def post(self, request):
        """
        Create a comment that is owned by user but can be attributed to any
        article.
        """
        request.data['comment']['owner'] = request.user.id
        serialized_comment = CommentSerializer(data=request.data['comment'])
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response({'comment': serialized_comment.data}, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """class for all requests that amend an existing comment with a particular pk"""

    def partial_update(self, request, pk):
        """Update request owned by the user"""
        # Remove owner from request object if get dict method returns True
        if request.data['comment'].get('owner', False):
            del request.data['comment']['owner']

        # Locate article
        # get_object_or_404 returns a object representation
        comment = get_object_or_404(Comment, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == comment.owner.id:
            raise PermissionDenied('Unauthorized, you are not the author of this comment!')

        # Add owner to data object now that we know this user owns the resource
        request.data['comment']['owner'] = request.user.id
        # Validate updates with serializer
        serialized_comment = CommentSerializer(comment, data=request.data['comment'], partial=True)
        if serialized_comment.is_valid():
            # Save & send a 204 no content
            serialized_comment.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(serialized_comment.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a comment owned by the user"""
        comment = get_object_or_404(Comment, pk=pk)
        if not request.user.id == comment.owner.id:
            raise PermissionDenied('Unauthorized, you are not the author of this comment!')
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

