# paiements/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaiementViewSet, BeneficeViewSet

router = DefaultRouter()
router.register(r'paiements', PaiementViewSet, basename='paiement')
router.register(r'benefices', BeneficeViewSet, basename='benefice')

urlpatterns = [
    path('', include(router.urls)),
]