"""Module for article views"""

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from ..models.article import Article
from ..serializers import \
    ArticleSerializer, \
    ArticleSerializerUnauthenticated, \
    MyArticleSerializer


# Create your views here.
class Articles(generics.ListCreateAPIView):
    """A class for getting an index of all articles and for creating a new article"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """Index request to get all articles"""
        # Get all the articles:
        articles = Article.objects.all().order_by('-created_at')
        # Run the data through the serializer
        serialized_article = ArticleSerializerUnauthenticated(articles, many=True)
        return Response({'articles': serialized_article.data})

    def post(self, request):
        """Create request to create one article"""
        # Add user to request data object
        request.data['article']['owner'] = request.user.id
        # Serialize/create article

        serialized_article = ArticleSerializer(data=request.data['article'])
        # If the data is valid according to our serializer...
        if serialized_article.is_valid():
            # Save the created article & send a response
            serialized_article.save()
            return Response({'article': serialized_article.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(serialized_article.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowArticle(generics.ListAPIView):
    """Class specifically for showing one article"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """Show request to return one article with pk"""
        # Locate the article to show
        article = get_object_or_404(Article, pk=pk)

        # Run the data through the serializer so it's formatted
        serialized_article = ArticleSerializer(article)
        return Response({'article': serialized_article.data})


class MyArticles(generics.ListAPIView):
    """A class for user specific requests"""

    def get(self, request):
        """Index request to get all articles created by user"""
        articles = Article.objects.all()
        my_articles = articles.filter(owner=request.user.id).order_by('-created_at')
        my_articles_serialized = MyArticleSerializer(my_articles, many=True)
        return Response({'my_articles': my_articles_serialized.data}, status=status.HTTP_200_OK)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """class for detailed pk specific http requests"""

    def delete(self, request, pk):
        """Delete request to delete one article with pk"""
        # Locate article to delete
        article = get_object_or_404(Article, pk=pk)
        # Check the article's owner is the user making this request
        if not request.user.id == article.owner.id:
            raise PermissionDenied('Unauthorized, you are not the author of this article!')
        # Only delete if the user owns the article
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update request to update one article with pk"""
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
        serialized_article = ArticleSerializer(article, data=request.data['article'], partial=True)
        if serialized_article.is_valid():
            # Save & send a 204 no content
            serialized_article.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(serialized_article.errors, status=status.HTTP_400_BAD_REQUEST)
