import uuid

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.authentication import UserJWTAuthentication
from .models import Form
from .serializers import FormSerializer
from .gcp_storage import upload_pdf_fileobj
from .paginations import FormsPagination

class UserFormsListView(ListAPIView):
    """Return a paginated list of forms belonging to the authenticated user."""
    authentication_classes = [UserJWTAuthentication]
    serializer_class = FormSerializer
    pagination_class = FormsPagination

    def get_queryset(self):
        """Limit results to the current user, newest first."""
        return Form.objects.filter(user=self.request.user).order_by("-created_at")

class SaveFormView(APIView):
    """Upload a PDF to GCP and create the corresponding Form record."""
    authentication_classes = [UserJWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """Handle multipart upload and persist the GCP URL on success."""
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response(
                {"detail": "file is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        title = request.data.get("title", "")
        object_name = f"forms/{request.user.id}/{uuid.uuid4()}.pdf"

        pdf_url = upload_pdf_fileobj(file_obj=file_obj, destination_path=object_name)

        form = Form.objects.create(
            user=request.user,
            title=title,
            pdf_bucket_url=pdf_url
        )

        return Response(
            FormSerializer(form).data, 
            status=status.HTTP_201_CREATED
        )


class UpdateFormView(APIView):
    """Replace the stored PDF and/or update metadata for a user's form."""
    authentication_classes = [UserJWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, form_id):
        """Upload a new PDF and/or update title for the selected form."""
        form = Form.objects.filter(id=form_id, user=request.user).first()
        if not form:
            return Response({"detail": "Form not found."}, status=status.HTTP_404_NOT_FOUND)

        file_obj = request.FILES.get("file")
        title = request.data.get("title")

        if not file_obj and title is None:
            return Response(
                {"detail": "Nothing to update. Provide file and/or title."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if file_obj:
            object_name = f"forms/{request.user.id}/{uuid.uuid4()}.pdf"
            pdf_url = upload_pdf_fileobj(file_obj=file_obj, destination_path=object_name)
            form.pdf_bucket_url = pdf_url

        if title is not None:
            form.title = title

        form.save(update_fields=["pdf_bucket_url", "title", "updated_at"])
        return Response(FormSerializer(form).data, status=status.HTTP_200_OK)
