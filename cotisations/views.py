# cotisations/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cycle
from .serializers import CycleSerializer


class CycleViewSet(viewsets.ModelViewSet):
    queryset = Cycle.objects.select_related('groupe', 'beneficiaire')
    serializer_class = CycleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['groupe', 'termine', 'beneficiaire']
    ordering_fields = ['numero', 'date_debut']
    ordering = ['numero']

    @action(detail=True, methods=['get'])
    def paiements(self, request, pk=None):
        cycle = self.get_object()
        from paiements.models import Paiement
        from paiements.serializers import PaiementSerializer
        paiements = Paiement.objects.filter(cycle=cycle)
        serializer = PaiementSerializer(paiements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        cycle = self.get_object()
        if cycle.termine:
            return Response(
                {"message": "Ce cycle est deja termine."},
                status=status.HTTP_400_BAD_REQUEST
            )
        total = sum(
            p.montant for p in cycle.paiements.filter(statut='paye')
        )
        cycle.montant_total = total
        cycle.termine = True
        cycle.save()
        return Response({
            "message": "Cycle termine avec succes !",
            "cycle": cycle.numero,
            "montant_total": float(total),
            "beneficiaire": str(cycle.beneficiaire),
        })

    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        total_cycles = Cycle.objects.count()
        termines = Cycle.objects.filter(termine=True).count()
        en_cours = Cycle.objects.filter(termine=False).count()
        return Response({
            'total_cycles': total_cycles,
            'termines': termines,
            'en_cours': en_cours,
        })