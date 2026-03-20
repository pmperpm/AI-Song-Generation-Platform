from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("users/", views.UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", views.UserRetrieveUpdateDestroyView.as_view(), name="user-detail"),
]