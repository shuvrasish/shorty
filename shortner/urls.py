from django.urls import path

from .views import URLSViewSet

urlpatterns = [path("url_shortner", URLSViewSet.as_view({"post": "create"}))]
