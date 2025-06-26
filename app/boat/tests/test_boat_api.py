"""
Tests for boat APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Boat

from boat.serializers import BoatSerializer


BOATS_URL = reverse('boat:boat-list')


def create_boat(user, **params):
    """Create and return a sample boat."""
    defaults = {
        'boat_name': 'Sample boat name',
        'boat_flag': 0,
        'home_port': 0,
    }
    defaults.update(params)

    boat = Boat.objects.create(user=user, **defaults)
    return boat


class PublicBoatAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(BOATS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateBoatAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_boats(self):
        """Test retrieving a list of boats."""
        create_boat(user=self.user)
        create_boat(user=self.user)

        res = self.client.get(BOATS_URL)

        boats = Boat.objects.all().order_by('-id')
        serializer = BoatSerializer(boats, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_boat_list_limited_to_user(self):
        """Test list of boats is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_boat(user=other_user)
        create_boat(user=self.user)

        res = self.client.get(BOATS_URL)

        boats = Boat.objects.filter(self.user)
        serializer = BoatSerializer(boats, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
