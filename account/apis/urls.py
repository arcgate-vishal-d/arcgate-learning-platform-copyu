from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("user/data/", views.AdminView.as_view(), name="UserData"),
    path("user/data/<int:pk>/", views.userDetail.as_view(), name="user-detail"),
    # path("user/<int:pk>/projects/", views.userDetail.as_view(), name="user-detail"),
    # path("user/data/<int:emp_id>/", views.userDetail.as_view(), name="user-detail"),
]
