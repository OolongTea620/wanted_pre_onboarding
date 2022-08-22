from django.urls import path
from users.views import SignInView,UserApplyView

urlpatterns = [
    path("", SignInView.as_view()),
    path("/signup", SignInView.as_view()),
    path("/apply", UserApplyView.as_view())
]