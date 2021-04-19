from django.urls import path
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword, GetUserDetails, UpdateUserDetails
from .views.article_views import Articles, ArticleDetail, MyArticles, ShowArticle, ArticlesSearch
from .views.comment_views import Comments, CommentDetail, MyComments
from .views.article_votes_views import ArticleVotes, ArticleVotesDetail
from .views.comment_votes_views import CommentVotes, CommentVotesDetail

urlpatterns = [
    # user paths
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('get-user-details/', GetUserDetails.as_view(), name='get-user-details'),
    path('update-user-details/', UpdateUserDetails.as_view(), name='update-user-details'),

    # article paths
    path('articles/', Articles.as_view(), name='articles'),
    path('articles/search/<slug:search_string>/', ArticlesSearch.as_view(), name='articles_filtered'),
    path('my-articles/', MyArticles.as_view(), name='my_articles'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('article/<int:pk>/', ShowArticle.as_view(), name='article'),

    # comment paths
    path('comments/', Comments.as_view(), name='comments'),
    path('comments/<int:pk>/', Comments.as_view(), name='comments-for-article'),
    path('my-comments/', MyComments.as_view(), name='my-comments'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),

    # paths for article votes
    path('article-votes/', ArticleVotes.as_view(), name='article_votes'),
    path('article-votes/<int:pk>/', ArticleVotesDetail.as_view(), name='article_votes_detail'),

    # paths for comment votes
    path('comment-votes/', CommentVotes.as_view(), name='comment_votes'),
    path('comment-votes/<int:pk>/', CommentVotesDetail.as_view(), name='comment_votes_detail'),
]
