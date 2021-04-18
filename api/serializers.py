from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models.article import Article
from .models.comment import Comment
from .models.article_votes import ArticleVote
from .models.comment_votes import CommentVote

class ArticleVotesSerializer(serializers.ModelSerializer):
    """A serializer class for votes on articles"""
    class Meta:
        model = ArticleVote
        fields = ('id', 'owner', 'article', 'vote')


class CommentVotesSerializer(serializers.ModelSerializer):
    """A serializer class for votes on comments"""
    class Meta:
        model = CommentVote
        fields = ('id', 'owner', 'comment', 'vote')


class CommentSerializer(serializers.ModelSerializer):
    """A serializer class for comments"""
    net_votes = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'body', 'article', 'owner', 'net_votes', 'author', 'created_at', 'updated_at')

    def get_net_votes(self, comment):
        comment_votes = comment.commentvote_set.all()

        net_votes = 0
        for key in comment_votes:
            net_votes += key.vote

        return net_votes

    def get_author(self, comment):
        return comment.owner.email


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the Article class"""
    comments = serializers.StringRelatedField(many=True, read_only=True)
    net_votes = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'sub_title',
            'img_url',
            'body',
            'comments',
            'net_votes',
            'created_at',
            'updated_at',
            'owner',
            'author',
            'comment_count'
        )

    def get_net_votes(self, article):
        article_votes = article.articlevote_set.all()

        net_votes = 0
        for key in article_votes:
            net_votes += key.vote

        return net_votes

    def get_author(self, article):
        """serializer method returning the owner email"""
        return article.owner.email

    def get_comment_count(self, article):
        """Serializer method returning the count of comments made on each article"""
        return article.comments.count()


class ArticleSerializerUnauthenticated(serializers.ModelSerializer):
    """A serializer class for unauthenticated users"""
    author = serializers.SerializerMethodField()
    net_votes = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'sub_title',
            'img_url',
            'author',
            'created_at',
            'net_votes',
            'comment_count'
        )

    def get_author(self, article):
        """serializer method returning the owner email"""
        return article.owner.email

    def get_net_votes(self, article):
        """serializer method return the net votes"""
        article_votes = article.articlevote_set.all()

        net_votes = 0
        for key in article_votes:
            net_votes += key.vote

        return net_votes

    def get_comment_count(self, article):
        """Serializer method returning the count of comments made on each article"""
        return article.comments.count()


class MyArticleSerializer(ArticleSerializerUnauthenticated):
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'sub_title',
            'img_url',
            'body',
            'comments',
            'author',
            'created_at',
            'updated_at',
            'net_votes',
            'comment_count'
        )


class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password', 'username', 'user_img_url')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 3}}

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)


class GetUserDetailsSerializer(serializers.ModelSerializer):
    """A class for returning user data that users are allowed to update"""
    class Meta:
        model = get_user_model()
        fields = ('username', 'user_img_url')

