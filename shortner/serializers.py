# serializers.py

from rest_framework import serializers

from .models import URLS


class URLSSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLS
        fields = ["original_url", "shortcode", "created_at"]


class URLShortenValidator(serializers.Serializer):
    url = serializers.URLField()
