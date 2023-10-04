from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("user/data/", views.UserListing.as_view(), name="UserData"),
]
