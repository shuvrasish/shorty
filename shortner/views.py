from django.db import IntegrityError
from django.db.utils import DataError
from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from shortner.models import URLS
from shortner.serializers import URLShortenValidator

# Create your views here.


class URLSViewSet(viewsets.ModelViewSet):
    help = """
        This view
    """

    def _get_short_url(self, request: HttpRequest, shortcode: str):
        """Constructs the short URL for the given shortcode.

        Args:
            request (HttpRequest): The HTTP request object.
            shortcode (str): The shortcode of the URL.

        Returns:
            str: The short URL.
        """
        server_url = request.build_absolute_uri("/")[:-1]
        return f"{server_url}/{shortcode}"

    def create(self, request: HttpRequest) -> Response:
        """Create a shortened URL.

        Args:
            request (HttpRequest): The HTTP request object containing the URL data.

        Returns:
            Response: Response containing the shortened URL.
        """
        try:
            validator = URLShortenValidator(data=request.data)
            if not validator.is_valid():
                raise ValidationError(validator.errors)
            original_url = validator.validated_data.get("url")
            shortcode = URLS.objects.shorten(original_url)
            url_obj = URLS(original_url=original_url, shortcode=shortcode)
            url_obj.save()
            short_url = self._get_short_url(request, shortcode)
            return Response({"data": url_obj.shortcode, "short_url": short_url})
        except IntegrityError as e:
            return Response(
                {"error": f"Internal Server Error: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except DataError as e:
            return Response(
                {"error": f"Data Error: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
