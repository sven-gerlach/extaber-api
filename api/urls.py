from django.urls import path
from .views.article_views import Articles, ArticleDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('articles/', Articles.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
]
