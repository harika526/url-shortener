from rest_framework import serializers
from .models import Links
from django.conf import settings



class LinksSerializer(serializers.ModelSerializer):
    full_short_url = serializers.SerializerMethodField()

    class Meta:
        model = Links
        fields = ('main_url', 'short_url', 'full_short_url', 'active')

    def get_full_short_url(self, obj):
        short_url = obj.short_url
        return settings.DEFAULT_DOMAIN+short_url
