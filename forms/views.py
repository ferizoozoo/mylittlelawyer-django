from rest_framework.generics import ListAPIView
from accounts.authentication import UserJWTAuthentication

from .models import Form
from .serializers import FormSerializer
from .paginations import FormsPagination


class UserFormsListView(ListAPIView):
    authentication_classes = [UserJWTAuthentication]
    serializer_class = FormSerializer
    pagination_class = FormsPagination

    def get_queryset(self):
        return Form.objects.filter(user=self.request.user).order_by("-created_at")
