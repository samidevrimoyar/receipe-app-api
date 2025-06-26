"""
Serializers for boat APIs.
"""
from rest_framework import serializers

from core.models import Boat


class BoatSerializer(serializers.ModelSerializer):
    """Serializer for boats."""

    class Meta:
        model = Boat
        fields = ['id', 'boat_name', 'boat_flag', 'home_port']
        read_only_fields = ['id']
