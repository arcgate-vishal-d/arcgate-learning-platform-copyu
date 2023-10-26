from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("users/", views.UserListing.as_view(), name="users"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("user/<int:user_id>/", views.UserDetail.as_view(), name="user_detail"),
    path(
        "user/update/",
        views.BulkUpdateUserDataView.as_view(),
        name="bulk_update_user_data",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
