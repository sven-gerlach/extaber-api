from django.urls import path
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.article_views import Articles, ArticleDetail
from .views.comment_views import Comments, CommentDetail
from .views.article_votes_views import ArticleVotes, ArticleVotesDetail
from .views.comment_votes_views import CommentVotes, CommentVotesDetail

urlpatterns = [
    # user paths
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),

    # article paths
    path('articles/', Articles.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),

    # comment paths
    path('comments/', Comments.as_view(), name='comments'),
    path('commensts/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),

    # paths for article votes
    path('article-votes/', ArticleVotes.as_view(), name='article_votes'),
    path('article-votes/<int:pk>/', ArticleVotesDetail.as_view(), name='article_votes_detail'),

    # paths for comment votes
    path('comment-votes/', CommentVotes.as_view(), name='comment_votes'),
    path('comment-votes/<int:pk>/', CommentVotesDetail.as_view(), name='comment_votes_detail'),
]
