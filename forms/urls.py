from django.urls import path

from .views import UserFormsListView

urlpatterns = [
    path("", UserFormsListView.as_view(), name="user-forms-list"),
]
