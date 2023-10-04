from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("user/data/", views.AdminView.as_view(), name="UserData"),
    path("user/<int:pk>/", views.userDetail.as_view(), name="user-detail"),
]
