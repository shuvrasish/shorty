from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from shortner.models import URLS


def index(request: HttpRequest) -> HttpResponse:
    """Render the index page."""
    return render(request, "index.html")


def redirect_to_long_url(request: HttpRequest, shortcode: str) -> HttpResponse:
    """Redirect to the original long URL using the provided shortcode."""
    url = get_object_or_404(URLS, shortcode=shortcode)
    return redirect(url.original_url)
