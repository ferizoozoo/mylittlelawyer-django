from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from accounts.authentication import UserJWTAuthentication

from .models import Form
from .serializers import FormSerializer


class FormsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserFormsListView(ListAPIView):
    authentication_classes = [UserJWTAuthentication]
    serializer_class = FormSerializer
    pagination_class = FormsPagination

    def get_queryset(self):
        return Form.objects.filter(user=self.request.user).order_by("-created_at")
