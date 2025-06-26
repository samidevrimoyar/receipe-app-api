"""
URL mappings for the boat app.
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from boat import views


router = DefaultRouter()
router.register('boats', views.BoatViewSet)

app_name = 'boat'

urlpatterns = [
    path('', include(router.urls)),
]