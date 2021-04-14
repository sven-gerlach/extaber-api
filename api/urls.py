from django.urls import path
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.article_views import Articles, ArticleDetail
from .views.comment_views import Comments, CommentDetail
from .views.article_votes_views import ArticleVotes

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('articles/', Articles.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('comments/', Comments.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
    path('article-votes/', ArticleVotes.as_view(), name='article_votes'),
]
