from types import MethodType
from django.urls import path
from postings.views import ArticleView, ArticleDetailView

urlpatterns = [
    path("", ArticleView.as_view()),
    path("/<int:posting_id>", ArticleView.as_view()),
    path("/detail/<int:posting_id>", ArticleDetailView.as_view()),
]