"""Module for article views"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.article import Article
from ..serializers import ArticleSerializer


# Create your views here.
class Articles(generics.ListCreateAPIView):
    """A class for getting an index of all articles and for creating a new article"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """Index request"""
        # Get all the articles:
        articles = Article.objects.all()
        # Run the data through the serializer
        serialized_article = ArticleSerializer(articles, many=True)
        return Response({'articles': serialized_article.data})

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['article']['owner'] = request.user.id
        # Serialize/create article
        serialized_article = ArticleSerializer(data=request.data['article'])
        # If the mango data is valid according to our serializer...
        if serialized_article.is_valid():
            # Save the created article & send a response
            serialized_article.save()
            return Response({'article': serialized_article.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(serialized_article.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """class for detailed pk specific http requests"""

    def get(self, request, pk):
        """Show request"""
        # Locate the article to show
        article = get_object_or_404(Article, pk=pk)

        # Run the data through the serializer so it's formatted
        serialized_article = ArticleSerializer(article)
        return Response({'article': serialized_article.data})

    def delete(self, request, pk):
        """Delete request"""
        # Locate article to delete
        article = get_object_or_404(Article, pk=pk)
        # Check the article's owner is the user making this request
        if not request.user.id == article.owner.id:
            raise PermissionDenied('Unauthorized, you are not the author of this article!')
        # Only delete if the user owns the article
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update request"""
        # Remove owner from request object if get dict method returns True
        if request.data['article'].get('owner', False):
            del request.data['article']['owner']

        # Locate article
        # get_object_or_404 returns a object representation
        article = get_object_or_404(Article, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == article.owner.id:
            raise PermissionDenied('Unauthorized, you are not the author of this article!')

        # Add owner to data object now that we know this user owns the resource
        request.data['article']['owner'] = request.user.id
        # Validate updates with serializer
        serialized_article = ArticleSerializer(article, data=request.data['article'])
        if serialized_article.is_valid():
            # Save & send a 204 no content
            serialized_article.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(serialized_article.errors, status=status.HTTP_400_BAD_REQUEST)
