# membres/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupeViewSet, MembreViewSet, AdhesionViewSet

router = DefaultRouter()
router.register(r'groupes', GroupeViewSet, basename='groupe')
router.register(r'membres', MembreViewSet, basename='membre')
router.register(r'adhesions', AdhesionViewSet, basename='adhesion')

urlpatterns = [
    path('', include(router.urls)),
]