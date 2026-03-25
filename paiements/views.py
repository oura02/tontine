# paiements/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Paiement, Benefice
from .serializers import PaiementSerializer, BeneficeSerializer


class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.select_related('membre', 'groupe', 'cycle')
    serializer_class = PaiementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['statut', 'moyen_paiement', 'groupe', 'membre']
    search_fields = ['membre__user__first_name', 'reference']
    ordering_fields = ['date_echeance', 'date_creation']
    ordering = ['-date_echeance']

    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        paiement = self.get_object()
        if paiement.statut == 'paye':
            return Response(
                {"message": "Ce paiement est deja confirme."},
                status=status.HTTP_400_BAD_REQUEST
            )
        paiement.statut = 'paye'
        paiement.date_paiement = timezone.now()
        paiement.save()
        return Response({
            "message": "Paiement confirme avec succes !",
            "reference": paiement.reference,
            "montant": float(paiement.montant),
            "date_paiement": paiement.date_paiement,
        })

    @action(detail=False, methods=['get'])
    def en_retard(self, request):
        from django.utils.timezone import now
        paiements = Paiement.objects.filter(
            statut='en_attente',
            date_echeance__lt=now().date()
        )
        serializer = self.get_serializer(paiements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        total = Paiement.objects.count()
        payes = Paiement.objects.filter(statut='paye').count()
        en_attente = Paiement.objects.filter(statut='en_attente').count()
        en_retard = Paiement.objects.filter(statut='en_retard').count()
        total_collecte = sum(
            p.montant for p in Paiement.objects.filter(statut='paye')
        )
        return Response({
            'total_paiements': total,
            'payes': payes,
            'en_attente': en_attente,
            'en_retard': en_retard,
            'total_collecte_fcfa': float(total_collecte),
        })


class BeneficeViewSet(viewsets.ModelViewSet):
    queryset = Benefice.objects.select_related('membre', 'cycle')
    serializer_class = BeneficeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['verse', 'membre']

    @action(detail=True, methods=['post'])
    def verser(self, request, pk=None):
        benefice = self.get_object()
        if benefice.verse:
            return Response(
                {"message": "Ce benefice a deja ete verse."},
                status=status.HTTP_400_BAD_REQUEST
            )
        benefice.verse = True
        benefice.date_versement = timezone.now()
        benefice.save()
        return Response({
            "message": "Benefice verse avec succes !",
            "membre": str(benefice.membre),
            "montant": float(benefice.montant),
        })