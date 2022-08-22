from django.urls import path
from companies.views import CompanyView

urlpatterns = [
    path("", CompanyView.as_view()),
    path("/register", CompanyView.as_view())
]